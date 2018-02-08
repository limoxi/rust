# -*- coding: utf-8 -*-

import settings

class CheckPointMiddleware(object):
	def process_request(sel, req, resp):
		"""
		检查是否需要经由中间价
		"""

		if len(filter(lambda path: path in req.path, settings.DIRECT_PATHS)) > 0:
			req.context['__middleware_passed'] = True