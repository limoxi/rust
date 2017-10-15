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
