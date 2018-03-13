#coding: utf8

from rust.command.base_command import BaseCommand
from rust.core.api import APPRESOURCE2CLASS
try:
	import api.resources #重要！误删！！
except:
	print ('no api yet')
from rust.apps import load_resources
load_resources()

from rust.resources.db.permission import models as permission_models

RESOURCE_METHODS = ['get', 'put', 'post', 'delete']
MANAGER_PERMISSION_GROUP = {
	'name': 'MANAGER',
	'desc': u'系统管理员'
}

class Command(BaseCommand):

	def handle(self, *args):
		"""
		初始化权限管理
		"""
		resources = {}

		for resource, data in APPRESOURCE2CLASS.items():
			if resource == 'permission':
				continue
			resources[resource] = []
			for method in  RESOURCE_METHODS:
				if getattr(data['cls'], method, None):
					resources[resource].append(method)

		need_delete_permission_ids = []
		resource2methods = dict()
		for rp in permission_models.Permission.select():
			resource = rp.resource
			resource2methods.setdefault(resource, []).append(rp.method)
			if resource not in resources.keys():
				need_delete_permission_ids.append(rp.id)
			else:
				if rp.method not in resources[resource]:
					need_delete_permission_ids.append(rp.id)

		#删除已经不存在的resource
		if len(need_delete_permission_ids) > 0:
			permission_models.Permission.delete().dj_where(id__in=need_delete_permission_ids).execute()
			permission_models.PermissionGroupHasPermission.delete().dj_where(permission_id__in=need_delete_permission_ids).execute()
			permission_models.UserLimitedPermission.delete().dj_where(permission_id__in=need_delete_permission_ids).execute()

		#增加新的权限
		create_list = []
		for resource, methods in resources.items():
			for method in methods:
				upper_method = method.upper()
				if upper_method not in resource2methods.get(resource, []):
					create_list.append(dict(
						resource = resource,
						method = upper_method
					))
		len(create_list) > 0 and permission_models.Permission.insert_many(create_list).execute()

		#创建默认权限分组
		if permission_models.PermissionGroup.select().dj_where(name=MANAGER_PERMISSION_GROUP['name']).count() == 0:
			permission_models.PermissionGroup.insert_many([MANAGER_PERMISSION_GROUP]).execute()

		#配置默认分组各自拥有的权限
		manager_group_id = permission_models.PermissionGroup.select().dj_where(name=MANAGER_PERMISSION_GROUP['name']).first().id
		permission_models.PermissionGroupHasPermission.delete().dj_where(group_id=manager_group_id).execute()
		need_create_group_permissions = []
		for rp in permission_models.Permission.select():
			need_create_group_permissions.append(dict(
				group_id = manager_group_id,
				permission_id = rp.id
			))
		len(need_create_group_permissions) > 0 and permission_models.PermissionGroupHasPermission.insert_many(need_create_group_permissions).execute()