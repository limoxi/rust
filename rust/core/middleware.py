
class BaseMiddleware(object):
    """
    falcon 中间件基类
    """
    def process_request(self, request, response):
        raise NotImplementedError

    def process_response(self, request, response, resource):
        raise NotImplementedError