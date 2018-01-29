# -*- coding: utf-8 -*-
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse #python3

from peewee import *
from peewee import Query
from playhouse.pool import PooledMySQLDatabase

def __parse_field_name(str):
    pos = str.find('__')
    if pos == -1:
        return str, None
    else:
        return str[:pos], str[pos:]

def dj_where(self, *expressions):
    self._where = self._add_query_clauses(self._where, expressions)

def django_where_returns_clone(func):

    def inner(self, *args, **kwargs):
        fields = self.model_class._meta.fields
        args = []
        for field_name, value in kwargs.items():
            field_name, op = __parse_field_name(field_name)
            db_field = fields.get(field_name, None)
            if not db_field and field_name.endswith('_id'):
                # maybe it's a foreign key
                field_name = field_name[:-3]
                db_field = fields.get(field_name, None)

            if not op:
                args.append(db_field.__eq__(value))
            else:
                if op == '__not':
                    args.append(db_field.__ne__(value))
                elif op == '__lt':
                    args.append(db_field.__lt__(value))
                elif op == '__lte':
                    args.append(db_field.__le__(value))
                elif op == '__gt':
                    args.append(db_field.__gt__(value))
                elif op == '__gte':
                    args.append(db_field.__ge__(value))
                elif op == '__notin':
                    if len(value) > 0:
                        args.append(db_field.not_in(value))
                elif op == '__icontains':
                    args.append(db_field.contains(value))
                elif op == '__range':
                    args.append(db_field.between(value[0], value[1]))
                elif op == '__in':
                    if len(value) == 0:
                        # TODO2: handle situations like "select * from table where id in ()"
                        value = ['-98765']
                    args.append(db_field.in_(value))
        kwargs = {}
        clone = self.clone()  # Assumes object implements `clone`.
        func(clone, *args, **kwargs)
        return clone

    inner.call_local = func  # Provide a way to call without cloning.
    return inner

Query.dj_where = django_where_returns_clone(dj_where)

class RetryOperationalError(object):
    def execute_sql(self, sql, params=None, require_commit=True):
        try:
            cursor = super(RetryOperationalError, self).execute_sql(
                sql, params, require_commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            cursor = self.get_cursor()
            cursor.execute(sql, params or ())
            if require_commit and self.get_autocommit():
                self.commit()
        return cursor


class MySQLDatabaseRetry(RetryOperationalError, MySQLDatabase):
    pass

schemes = {
    'mysql': MySQLDatabase,
    'mysql+retry': MySQLDatabaseRetry,
    'mysql+pool': PooledMySQLDatabase,
}


def parse_result_to_dict(parsed):
    connect_kwargs = {'database': parsed.path[1:]}
    if parsed.username:
        connect_kwargs['user'] = parsed.username
    if parsed.password:
        connect_kwargs['password'] = parsed.password
    if parsed.hostname:
        connect_kwargs['host'] = parsed.hostname
    if parsed.port:
        connect_kwargs['port'] = parsed.port

    # Adjust parameters for MySQL.
    if parsed.scheme == 'mysql' and 'password' in connect_kwargs:
        connect_kwargs['passwd'] = connect_kwargs.pop('password')

    return connect_kwargs


def connect(url, **connect_params):
    parsed = urlparse(url)
    connect_kwargs = parse_result_to_dict(parsed)
    connect_kwargs.update(connect_params)
    database_class = schemes.get(parsed.scheme)

    if database_class is None:
        if database_class in schemes:
            raise RuntimeError('Attempted to use "%s" but a required library '
                               'could not be imported.' % parsed.scheme)
        else:
            raise RuntimeError('Unrecognized or unsupported scheme: "%s".' %
                               parsed.scheme)

    return database_class(**connect_kwargs)
