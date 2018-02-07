#coding: utf8

from rust.command.base_command import BaseCommand
from rust.core.api_resource import APPRESOURCE2CLASS

import api.resources #重要！误删！！
from rust.apps import load_rust_resources
load_rust_resources()

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

		for resource_name, data in APPRESOURCE2CLASS.items():
			if resource_name == 'permission':
				continue
			resources[resource_name] = []
			for method in  RESOURCE_METHODS:
				if getattr(data['cls'], method, None):
					resources[resource_name].append(method)
		print resources

		need_delete_permission_ids = []
		resource2methods = dict()
		for rp in permission_models.ResourcePermission.select():
			resource_name = rp.resource_name
			resource2methods.setdefault(resource_name, []).append(rp.method)
			if resource_name not in resources.keys():
				need_delete_permission_ids.append(rp.id)
			else:
				if rp.method not in resources[resource_name]:
					need_delete_permission_ids.append(rp.id)

		#删除已经不存在的resource
		permission_models.ResourcePermission.delete().dj_where(id__in=need_delete_permission_ids).execute()
		permission_models.PermissionGroupHasPermission.delete().dj_where(resource_permission_id__in=need_delete_permission_ids).execute()
		permission_models.UserLimitedPermission.delete().dj_where(resource_permission_id__in=need_delete_permission_ids).execute()

		#增加新的权限
		create_list = []
		for resource_name, methods in resources.items():
			for method in methods:
				upper_method = method.upper()
				if upper_method not in resource2methods.get(resource_name, []):
					create_list.append(dict(
						resource_name = resource_name,
						method = upper_method
					))
		len(create_list) > 0 and permission_models.ResourcePermission.insert_many(create_list).execute()

		#创建默认权限分组
		if permission_models.PermissionGroup.select().dj_where(name=MANAGER_PERMISSION_GROUP['name']).count() == 0:
			permission_models.PermissionGroup.insert_many([MANAGER_PERMISSION_GROUP]).execute()

		#配置默认分组各自拥有的权限
		manager_group_id = permission_models.PermissionGroup.select().dj_where(name=MANAGER_PERMISSION_GROUP['name']).first().id
		permission_models.PermissionGroupHasPermission.delete().dj_where(group_id=manager_group_id).execute()
		need_create_group_permissions = []
		for rp in permission_models.ResourcePermission.select():
			need_create_group_permissions.append(dict(
				group_id = manager_group_id,
				resource_permission_id = rp.id
			))
		len(need_create_group_permissions) > 0 and permission_models.PermissionGroupHasPermission.insert_many(need_create_group_permissions).execute()

