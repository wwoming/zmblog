"""==========zhuming=========="""

from flask import Blueprint, render_template, redirect, url_for, request

# 创建管理前端的蓝图对象
from back.models import Article

web_blue = Blueprint('web', __name__)


# 首页
@web_blue.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # 倒序排列文章，最新文章就放5个
        articles = Article.query.order_by(-Article.id).all()
        return render_template('web/index.html', articles=articles)


# 阅读全文/展示全文的页面
@web_blue.route('/info/<int:id>/', methods=['GET', 'POST'])
def info(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        articles = Article.query.all()
        # 在数据库中id的自动生成有可能被人为的打断顺序，所以不能直接通过对于id的加减进行查询
        # 只能通过取出所有id保存在列表中，根据下标的加减来查询
        ids = [art.id for art in articles]
        # 判断是否只有一篇文章
        pre_article = ''
        if len(ids) > 1:
            pre_id = ids[ids.index(id) - 1]
            pre_article = Article.query.get(pre_id)
        # 判断是否为最后一篇
        next_article = ''
        if id != max(ids):
            next_id = ids[ids.index(id) + 1]
            next_article = Article.query.get(next_id)
        return render_template('web/info.html', article=article,
                               ids=ids, pre_article=pre_article, next_article=next_article)


# 文章列表
@web_blue.route('/list/<int:id>', methods=['GET', 'POST'])
def art_list(id):
    if request.method == 'GET':
        arts = Article.query.order_by(-Article.id).all()
        if id < 1:
            id = 1
        if id*4 > len(arts):
            id = len(arts)//4 + 1
        page = id
        articles = Article.query.order_by(-Article.id).offset((page-1)*4).limit(4).all()
        return render_template('web/list.html', articles=articles, id=id, arts=arts)


# 关于我
@web_blue.route('/about/', methods=['GET', 'POST'])
def about():

    return render_template('web/about.html')


# 留言
@web_blue.route('/gbook/', methods=['GET', 'POST'])
def gbook():

        return render_template('web/gbook.html')




















