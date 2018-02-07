#coding: utf8

from rust.core.api_resource import ApiResource, ParamObject
from rust.core.decorator import param_required

from rust.resources.business.user.user_factory import UserFactory

class AUser(ApiResource):
	"""
	用户
	"""
	app = 'rust.user'
	resource = 'user'

	@param_required(['user', 'name', 'password'])
	def put(params):
		param_object = ParamObject({
			'name': params['name'],
			'password': params['password']
		})
		user = UserFactory().create(param_object)
		return {
			'id': user.id
		}

	@param_required(['user', '?nick_name', '?password', '?avatar'])
	def post(params):
		param_object = ParamObject({
			'nick_name': params.get('nick_name'),
			'password': params.get('password'),
			'avatar': params.get('avatar')
		})
		UserFactory(params['user']).update(param_object)
		return {}