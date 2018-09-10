# rust - 基于falcon的web框架

### 依赖
``可查看目录下 'requirements.txt' ``

### 安装
``pip install -U git+https://github.com/limoxi/rust.git``

### TODO
- [x] 自带user和permission资源
- [x] 分页工具
- [x] 暂只接收application/x-www-form-urlencoded、application/json、application/xml 三种类型数据
- [x] 支持白名单形式的跨域设置
- [ ] 加入behave支持
- [x] 初始化项目命令 rust-cli init xxx
- [x] 增加资源命令 rust-cli add xxx
- [ ] 支持多种数据库，并提供扩展能力
- [ ] 支持容器部署
- [ ] python3支持
- [ ] api请求日志(异步)
- [ ] 完善文档


### 项目参考
>[python书写风格指南](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)  
>[《实现领域驱动设计》[美] Vaughn Vernon 著；滕云 译](https://item.jd.com/11423256.html)  
>[falcon](https://github.com/falconry/falcon)  

### 升级日志
v 1.1.1
- 升级peewee=v3.6.4
    - db_table 改为 table_name
- 升级falcon=1.4.1
- 升级PyMySQL=0.9.2