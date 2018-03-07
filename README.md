# rust - 基于falcon的web框架

### 依赖
``可查看目录下 'requirements.txt' ``

### 安装
``pip install -U git+https://github.com/limoxi/rust.git``

### TODO
- [x] 自带user和permission资源
- [x] 分页工具
- [ ] 接收text/plain、application/x-www-form-urlencoded、application/json、application/xml四种类型数据
- [x] 支持白名单形式的跨域设置
- [ ] 加入behave支持
- [x] 初始化项目命令 rust-cli init_project xxx
- [x] 增加资源命令 rust-cli add_resource xxx
- [ ] 同时支持mysql、mongodb，并将peewee和mongoengine的数据库操作封装成统一方法
- [ ] python3支持
- [ ] api请求日志(异步)
- [ ] 完善文档