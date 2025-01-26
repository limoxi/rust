from rust import Config

if __name__ == '__main__':
    print(1, '==>>', Config.get_raw())
    print(2, '==>>', Config.get_int('jwt.expire_seconds', 2*60*60))
    print(3, '==>>', Config.get_list('rust.middleware.middlewares'))
    print(4, '==>>', Config.get_list('rust.cors.white_list'))
    print(5, '==>>', Config.get_list('rust.resources'))
    print(6, '==>>', Config.get_list('rust.middleware.ignored_paths'))
    print(7, '==>>', Config.get_str('default_auth_password', '123456'))
    print(8, '==>>', Config.get_str('jwt.secret', 'aSsJKgdAH2Dkaj1shd4ahsh'))
    print(9, '==>>', Config.get_list('db'))