
class BaseMiddleware(object):
    """
    falcon 中间件基类
    """
    def process_request(self, req, resp):
        raise NotImplementedError

    def process_response(self, req, resp, resource, req_succeeded):
        raise NotImplementedError