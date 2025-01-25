import json

from rust.core.exceptions import ApiParameterError

class cached_context_property(property):
    """
    用于指定一个可以被context缓存的decorator
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        property.__init__(self, fget, fset, fdel, doc)

        self.func = fget
        self.func_name = fget.__name__

    def __get__(self, instance, type=None):
        if instance is None:
            return self

        value = instance.context.get(self.func_name, None)
        if value == None:
            value = self.func(instance)
            instance.context[self.func_name] = value
        return value

    def __set__(self, instance, value):
        instance.context[self.func_name] = value

def param_required(params=None):
    """
    用于检查函数参数的decorator
    1. name,表示为必须参数
    2. name:type,表示自动类型转换，支持"str","int","float","bool","json"。其中bool识别True/False,"True"/"False","true"/"false"
    3. ?name,以?开头的参数，表示非必须参数
    """
    def wrapper(function):
        def inner(self):
            data = self.params
            for param in params:
                if ':' in param:
                    param_name, param_type = param.split(':')
                else:
                    param_name = param
                    param_type = None
                if '?' in param_name:
                    param_name = param_name.replace('?', '')
                    is_required = False
                else:
                    is_required = True

                if is_required and param_name not in data:
                    raise ApiParameterError('Required parameter missing: %s' % param_name)

                try:

                    if param_type and param_name in data:
                        param_value = data[param_name]
                        if param_type == "int":
                            data[param_name] = int(param_value)
                        elif param_type == 'bool':
                            data[param_name] = param_value in ("True", "true", True)
                        elif param_type == "float":
                            data[param_name] = float(param_value)
                        elif param_type == "json":
                            data[param_name] = json.loads(param_value)
                except BaseException as e:
                    raise ApiParameterError('Invalid parameter: %s is not %s.%s' % (param_name, param_type, e.message))

            return function(self)

        return inner

    return wrapper