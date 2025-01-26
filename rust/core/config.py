import os

from ruamel.yaml import YAML

from rust.utils.map import Map

def _replace_env_vars(data):
    """
    替换环境变量
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                sps = value.strip()[2:-1].split('||')
                env_var = sps[0]
                default_var = sps[1] if len(sps) == 2 else ''
                data[key] = os.environ.get(env_var, default_var)
            elif isinstance(value, (dict, list)):
                _replace_env_vars(value)
    elif isinstance(data, list):
        for item in data:
            _replace_env_vars(item)

class __Config(Map):
    def __init__(self, dict_data):
        _replace_env_vars(dict_data)
        super().__init__(dict_data)

    def is_dev(self):
        return self.get_str('mode') == 'dev'
    def is_test(self):
        return self.get_str('mode') == 'test'
    def is_prod(self):
        return self.get_str('mode') == 'prod'


def load_config():
    config_path = os.path.join('config', 'config.yaml')
    with open(config_path, 'r', encoding='utf8') as f:
        try:
            data = YAML().load(f)
            return __Config(data)
        except Exception as e:
            raise Exception(f'配置文件内容错误: {config_path} : {e}')

    return None