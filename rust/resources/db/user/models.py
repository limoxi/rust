#coding: utf8

from rust.core import db as models

class User(models.Model):
    """
    用户
    """
    username = models.CharField(default='', max_length=128) #用户名
    password = models.CharField(default='', max_length=1024) #密码
    nickname = models.CharField(default='', max_length=512) #用户昵称
    avatar = models.TextField(default='') #头像
    is_manager = models.BooleanField(default=False) # 是否管理员
    created_at = models.DateTimeField(auto_now_add=True) #创建时间

    class Meta(object):
        table_name = 'rust_user'