#coding: utf8

from rust.core import db as models

class Permission(models.Model):
    """
	资源权限
	"""
    resource = models.CharField(default='', max_length=128)  # 资源名
    method = models.CharField(default='GET', max_length=32)  # 方法名
    created_at = models.DateTimeField(auto_now_add=True)  # 更新时间

    class Meta(object):
        table_name = 'rust_permission'


class PermissionGroup(models.Model):
    """
	权限组
	"""
    name = models.CharField(default='', max_length=512, unique=True)  # 组名
    desc = models.CharField(default='', max_length=1024)  #描述

    class Meta(object):
        table_name = 'rust_permission_group'

class PermissionGroupHasPermission(models.Model):
    """
	权限组拥有的权限
	"""
    group_id = models.IntegerField(default=0)
    permission_id = models.IntegerField(default=0)

    class Meta(object):
        table_name = 'rust_permission_group_has_permission'


class PermissionGroupHasUser(models.Model):
    """
	权限组中的用户
	"""
    group_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    updated_at = models.DateTimeField(null=False)

    class Meta(object):
        table_name = 'rust_permission_group_has_user'


class UserLimitedPermission(models.Model):
    """
	用户禁止访问的资源及方法
	"""
    user_id = models.IntegerField(default=0)
    permission_id = models.IntegerField(default=0)
    updated_at = models.DateTimeField()  # 更新时间

    class Meta(object):
        table_name = 'rust_user_limited_permission'