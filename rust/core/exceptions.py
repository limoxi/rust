# -*- coding: utf-8 -*-

def __full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if not exc is None:  # i.e. if an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last, REVERSED CALL ORDER):\n'
    stack_str = trc + ''.join(reversed(traceback.format_list(stack)))
    if not exc is None:
        stack_str += '  ' + traceback.format_exc().lstrip(trc)

    return stack_str

def unicode_full_stack():
    return __full_stack().decode('utf-8')

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

    def __init__(self, app, resource, method):
        self.code = 404
        self.message = 'api===>{}.{}.{} not exist'.format(app, resource, method)
        super(ApiNotExistError, self).__init__(self.message)

class ApiParameterError(Exception):

    def __init__(self, message):
        self.code = 530
        self.message = message
        super(ApiParameterError, self).__init__(message)