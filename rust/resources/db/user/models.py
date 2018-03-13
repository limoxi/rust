#coding: utf8

from rust.core import db as models

class User(models.Model):
    """
    用户
    """
    name = models.CharField(default='', max_length=128) #用户名
    password = models.CharField(default='', max_length=1024) #密码
    nick_name = models.CharField(default='', max_length=512) #用户昵称
    avatar = models.TextField(default='') #头像
    created_at = models.DateTimeField(auto_now_add=True) #创建时间

    class Meta(object):
        db_table = 'rust_user'

class UserSession(models.Model):
    """
    用户登录会话
    """
    user_id = models.IntegerField(default=0)
    session_key = models.CharField(max_length=40, primary_key=True)
    expire_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta(object):
        db_table = 'rust_user_session'