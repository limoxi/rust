# -*- coding: utf-8 -*-

def __full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    if not exc is None:  # i.e. if an exception is present
        del stack[-1]       # remove call of full_stack, the printed exception
        # will contain the caught exception caller instead
    trc = 'Traceback (most recent call last, REVERSED CALL ORDER):\n'
    stackstr = trc + ''.join(reversed(traceback.format_list(stack)))
    if not exc is None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)

    return stackstr

def unicode_full_stack():
    return __full_stack().decode('utf-8')


class BusinessError(Exception):
    """
    business层的异常，用于在api层被捕获
    """
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, message)

    def __unicode__(self):

        return u"{}".format(self.message)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def get_message(self, en2name=None):
        if not en2name:
            return self.message
        return en2name.get(self.message, u'business error')