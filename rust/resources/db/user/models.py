
from rust.core import db as models

class User(models.Model):
    """
    用户
    """
    name = models.CharField(default='', max_length=512)  # 用户昵称
    avatar = models.TextField(default='')   # 头像
    created_at = models.DateTimeField(auto_now_add=True)    # 创建时间

    class Meta(object):
        table_name = 'rust_user'

class UserLoginProfile(models.Model):
    """
    用户登录渠道
    """
    user_id = models.IntegerField()
    channel = models.CharField(default='username')  # 登录渠道
    login_key = models.CharField(max_length=1024, default='')
    login_secret = models.CharField(max_length=1024, default='')
    extra_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta(object):
        table_name = 'rust_user_login_profile'