import traceback, sys

def print_full_stack():
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]
    if not exc is None:
        del stack[-1]
    trc = 'Traceback (most recent call last, REVERSED CALL ORDER):\n'
    stack_str = trc + ''.join(reversed(traceback.format_list(stack)))
    if not exc is None:
        stack_str += '  ' + traceback.format_exc().lstrip(trc)

    print(stack_str)

class __EncodedException(Exception):

    __slots__ = (
        'code',
        'message',
    )

    def get_message(self):
        return self.message

class BusinessError(__EncodedException):
    """
    业务异常
    """
    def __init__(self, message):
        self.code = 531
        self.message = message
        super(BusinessError, self).__init__(message)

class ApiNotExistError(Exception):

    def __init__(self, resource, method):
        self.code = 404
        self.message = 'api===>{}.{} not exist'.format(resource, method)
        super(ApiNotExistError, self).__init__(self.message)

class ApiParameterError(Exception):

    def __init__(self, message):
        self.code = 530
        self.message = message
        super(ApiParameterError, self).__init__(message)