"""==========zhuming=========="""

from functools import wraps
from flask import session, redirect, url_for

from back.models import User


# 判断是否已经登录的装饰器，里面的func就是被装饰的函数，
# 内层函数返回外层函数的参数(即被装饰的函数)，如果被装饰的函数有参数，那内层函数应该有不定长参数
def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('back.login'))
    return check

