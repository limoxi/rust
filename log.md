# rust - 版本日志

### 版本号格式
```
主版本.子版本.修订版次.日期_版本阶段
```

#### 版本阶段
```
Alpha   内部开发版
Beta    公开测试
Release 正式版
```

### 升级日志
> v0.4.2.190422_Alpha
- 修复PermissionGroup唯一性索引名太长的问题
- 删除权限中间件的遗留代码

> v0.4.1.190406_Alpha
- 增强peewee，增加自定义FieldType
    - ListField
    - DictField
- 修复一些问题

> v0.4.0.190330_Alpha
- 重构api层，优化资源实现
    ```python
    from rust.core.api import ApiResource, Resource
    from rust.core.decorator import param_required

    @Resource('test.test')
    class ATest(ApiResource):

        @param_required(['id'])
        def get(self):
            return {
                'success': True
            }
    ```
- 重构代码生成器

> v0.3.7.190325_Alpha
- 优化异常处理
    - 统一业务逻辑异常: BusinessError
    - 去除BusinessException
    - api层不再支持return 500类的返回值，错误处理一概使用raise抛出
    
> v0.3.6.190316_Alpha
- 增强peewee的order_by方法，使支持字符串表达，例如：
    ```
    user_models.User.select().order_by(['-id', 'updated_at'])
    ```
- 修复不识别content_type为application/json时的问题
    - 因为当前版本falcon的MEDIA_JSON为'application/json; charset=UTF-8'

> v0.3.5.190213_Alpha
- 取消加入behave支持的计划，BDD功能将由独立服务iBehave提供
- 重新设计领域事件机制，仅支持异步事件(通过消息服务实现),同步事件直接使用service调用，降低代码复杂度
    - (TODO)提供console、redis两种异步消息处理器，并支持自定义处理器
    - 异步事件将在数据库事务提交后按顺序逐一发送
- 默认加载中间件错误处理器
    - 在中间件中处理错误信息可以直接抛出MiddlewareException异常
- 一些小优化

> v0.3.4.190211_Alpha
- 调整分页器类初始化逻辑
- 完善内建user模块的功能
- 修复CORS支持功能的小问题

> v0.3.2.190128_Alpha
- 调整默认权限分组存储方案
- 修复获取token问题
- 修复分组名称重复问题

> v0.3.0.190127_Alpha
- 增加用户注册功能
- 增加修改用户信息功能
- 增加修改密码功能
- 修复dj_where无效的问题
- 修复接口错误信息不全的问题

> v0.2.0.190116_Alpha
- 事务支持
    - 为每个api请求开启一个事务
- 完善权限分组功能
- 完善登陆流程
- JWT机制校验用户登陆，代替旧的session_key方案
- 修复一些问题

> v 0.1.0.171016_Alpha
- 升级peewee=v3.6.4
    - db_table 改为 table_name
- 升级falcon=1.4.1
- 升级PyMySQL=0.9.2