from flask import Flask, session, render_template, redirect, Blueprint, request, jsonify, url_for
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# 导入所有子路由创建函数
from .spider import create_spider_routes
from .delete import create_delete_routes
from .analyse import create_analyse_routes
from .char import create_char_routes
from .data import create_data_routes

# 检查模板文件夹位置
template_folder_path = os.path.join(os.path.dirname(__file__), '..', '..', 'views', 'page', 'templates')
if not os.path.exists(template_folder_path):
    # 如果不存在，使用默认的templates
    template_folder_path = 'templates'

page_app = Blueprint('page', __name__, url_prefix='/page', template_folder=template_folder_path)

# 注册所有子路由
create_spider_routes(page_app)
create_delete_routes(page_app)
create_analyse_routes(page_app)
create_char_routes(page_app)
create_data_routes(page_app)

# 主页面路由
@page_app.route('/home')
def home():
    from utils.base_page import getHomeTagsData, getHomeCommentsLikeCountTopFore, getHomeArticleCreatedAtChart, getHomeTypeChart, getEmotion
    
    username = session.get('username')
    try:
        articleLenMax, likeCountMaxAuthorName, cityMax, articleList = getHomeTagsData()
        commentsLikeCountTopFore = getHomeCommentsLikeCountTopFore()
        xData, yData = getHomeArticleCreatedAtChart(articleList)
        typeChart = getHomeTypeChart(articleList)
        emotionData = getEmotion()
        
        return render_template('index.html',
                               username=username,
                               articleLenMax=articleLenMax,
                               likeCountMaxAuthorName=likeCountMaxAuthorName,
                               cityMax=cityMax,
                               commentsLikeCountTopFore=commentsLikeCountTopFore,
                               xData=xData,
                               yData=yData,
                               typeChart=typeChart,
                               emotionData=emotionData
                               )
    except Exception as e:
        print(f"Home page error: {e}")
        return render_template('index.html', username=username, error="数据加载失败")

@page_app.route('/')
def page_index():
    return redirect('/page/home')


