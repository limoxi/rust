
from rust.core import business

class PermissionGroupEncodeService(business.Service):

	def encode(self, group):
		if not group:
			return {}
		return {
			'id': group.id,
			'name': group.name,
			'desc': group.desc,
		}
