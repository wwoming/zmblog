"""==========zhuming=========="""

from functools import wraps
from flask import session, redirect, url_for


# 判断是否已经登录的装饰器，里面的func就是被装饰的函数
def is_login(func):
    @wraps(func)
    def check():
        if 'user_id' in session:
            return func()
        return redirect(url_for('back.login'))
    return check

