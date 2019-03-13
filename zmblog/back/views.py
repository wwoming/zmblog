

from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import User, db, Article, Article_type
from utils.functions import is_login

# 创建管理后台的蓝图对象
back_blue = Blueprint('back', __name__)


@back_blue.route('/index/')
@is_login
def index():
    return render_template('/back/index.html')


@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该用户名已被注册，请重新注册'
                return render_template('back/register.html', error=error)
            if password != password2:
                error = '请确认两次输入密码相同'
                return render_template('back/register.html', error=error)
            # 添加数据
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            user.save()
            return redirect(url_for('back.login'))
        else:
            error = '请输入完整信息'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if not user:
            error = '该用户没有注册，请前往注册'
            return render_template('back/login.html', error=error)
        if not check_password_hash(user.password, password):
            error = '密码错误，请重新输入'
            return render_template('back/login.html', error=error)
        # 用户名和密码都对，设置session
        session['user_id'] = user.id
        return redirect(url_for('back.index'))


# 注销
@back_blue.route('/logout/')
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


# 用户列表
@back_blue.route('/user_list/', methods=['GET', 'POST'])
@is_login
def user_list():
    if request.method == 'GET':
        users = User.query.all()
        # 取出没有被删除的用户
        users = [user for user in users if user.is_delete == 0]
        return render_template('back/user_list.html', users=users)


# 删除用户
@back_blue.route('/del_user/<int:id>/', methods=['GET', 'POST'])
# @is_login  # 这里如果不判断是否已经登录，那就算没有登录也可以直接输入路由地址删除用户
def del_user(id):
    # 删除用户，直接访问路由能删吗？ 好像不能
    # 删除用户的同时应该删除对应的session,但是这里删除session,就所有账号的都删了，就会返回登录界面，应该要有个超级管理员
    # del session['user_id']
    if not session['user_id']:
        return redirect(url_for('back.login'))
    user = User.query.get(id)
    user.is_delete = 1
    return redirect(url_for('back.user_list'))


# 文章分类
@back_blue.route('/article_category_list/', methods=['GET', 'POST'])
@is_login
def article_category_list():
    if request.method == 'GET':
        art_types = Article_type.query.all()
        return render_template('back/article_category_list.html', art_types=art_types)


# 添加文章分类
@back_blue.route('/add_article_category/', methods=['GET', 'POST'])
@is_login
def add_article_category():
    if request.method == 'GET':
        return render_template('back/add_article_category.html')
    if request.method == 'POST':
        category = request.form.get('category')
        if category:
            # 判断有没有和已有的分类名重复
            article_type = Article_type.query.filter(Article_type.tp_name == category).first()
            if article_type:
                error = '该分类名已存在，请重新输入'
                return render_template('back/add_article_category.html', error=error)
            # 保存分类信息
            art_type = Article_type()
            art_type.tp_name = category
            art_type.save()
            return redirect(url_for('back.article_category_list'))
        error = '请输入分类信息'
        return render_template('back/add_article_category.html', error=error)


# 删除文章分类
@back_blue.route('/del_art_category/<int:id>/', methods=['GET', 'POST'])
def del_art_category(id):
    if not session['user_id']:
        return redirect(url_for('back.login'))
    art_type = Article_type.query.get(id)
    art_type.delete()
    return redirect(url_for('back.article_category_list'))


# 修改文章分类
@back_blue.route('/update_category/<int:id>/', methods=['GET', 'POST'])
def update_category(id):
    if request.method == 'GET':
        if not session['user_id']:
            return redirect(url_for('back.login'))
        art_type = Article_type.query.get(id)
        return render_template('back/add_article_category.html', art_type=art_type)
    if request.method == 'POST':
        category = request.form.get('category')
        if category:
            # 判断有没有和已有的分类名重复
            article_type = Article_type.query.filter(Article_type.tp_name == category).first()
            if article_type:
                error = '该分类名已存在，请重新输入'
                return render_template('back/add_article_category.html', error=error)
            # 保存分类信息
            art_type = Article_type.query.get(id)
            art_type.tp_name = category
            art_type.save()
            return redirect(url_for('back.article_category_list'))
        error = '请输入分类信息'
        return render_template('back/add_article_category.html', error=error)


# 文章列表
@back_blue.route('/article_list/', methods=['GET', 'POST'])
@is_login
def article_list():
    if request.method == 'GET':
        articles = Article.query.order_by(-Article.id).all()
        return render_template('back/article_list.html', articles=articles)


# 添加文章
@back_blue.route('/add_article/', methods=['GET', 'POST'])
@is_login
def add_article():
    if request.method == 'GET':
        art_types = Article_type.query.all()
        return render_template('back/add_article.html', art_types=art_types)
    if request.method == 'POST':
        title = request.form.get('title')
        tp_id = request.form.get('type')
        desc = request.form.get('desc')
        content = request.form.get('content')
        if title and type and desc and content:
            # 判断标题有没有重复的
            article = Article.query.filter(Article.title == title).first()
            if article:
                error = '该标题已存在，请重新编辑'
                art_types = Article_type.query.all()
                return render_template('back/add_article.html', error=error, art_types=art_types)
            article = Article()
            article.title = title
            article.tp_id = tp_id
            article.desc = desc
            article.content = content
            article.save()
            return redirect(url_for('back.article_list'))
        error = '请填写完整信息'
        art_types = Article_type.query.all()
        return render_template('back/add_article.html', error=error, art_types=art_types)


# 删除文章
@back_blue.route('/del_article/<int:id>', methods=['GET', 'POST'])
def del_article(id):
    if not session['user_id']:
        return redirect(url_for('back.login'))
    article = Article.query.get(id)
    article.delete()
    return redirect(url_for('back.article_list'))


# 修改文章
@back_blue.route('/update_article/<int:id>', methods=['GET', 'POST'])
def update_article(id):
    if request.method == 'GET':
        if not session['user_id']:
            return redirect(url_for('back.login'))
        # 获取所有分类
        art_types = Article_type.query.all()
        # 获取文章对象
        article = Article.query.get(id)
        return render_template('back/add_article.html', art_types=art_types, article=article)
    if request.method == 'POST':
        title = request.form.get('title')
        tp_id = request.form.get('type')
        desc = request.form.get('desc')
        content = request.form.get('content')
        if title and type and desc and content:
            # 判断标题有没有和别的标题重复的，这里不包括被修改的文章本身
            article = Article.query.filter(Article.title == title).first()
            original_title = Article.query.get(id).title
            if article and article.title != original_title:
                error = '该标题已存在，请重新编辑'
                art_types = Article_type.query.all()
                article = Article.query.get(id)
                return render_template('back/add_article.html', error=error, art_types=art_types, article=article)
            article = Article.query.get(id)
            article.title = title
            article.tp_id = tp_id
            article.desc = desc
            article.content = content
            article.save()
            return redirect(url_for('back.article_list'))
        error = '请填写完整信息'
        art_types = Article_type.query.all()
        return render_template('back/add_article.html', error=error, art_types=art_types)


@back_blue.route('/', methods=['GET', 'POST'])
def editor():
    #如果是post方法就返回tinymce生成html代码，否则渲染editor.html
    if request.method=='POST':
        return request.form['content']
    return render_template('back/editor.html')
