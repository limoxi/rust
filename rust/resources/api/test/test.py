
from rust.core.api import ApiResource, Resource
from rust.core.decorator import param_required

@Resource('test.test')
class Test(ApiResource):

	@param_required(['id'])
	def get(self):

		return {
			'success': True
		}