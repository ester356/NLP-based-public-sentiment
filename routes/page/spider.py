
from flask import session, render_template, request, redirect, url_for
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_spider_routes(blueprint):
    # 爬取指定文章
    @blueprint.route('/spiderArticle', methods=['GET'])
    def spiderArticle():
        from spiders.main import main_2
        
        message = ''
        username = session.get('username')
        url = request.args.get('url')
        type_str = request.args.get('type')
        try:
            if url:
                if not url.startswith('https://weibo.com/'):
                    message = '地址错误'
                    return render_template('spiderData.html',
                                           username=username,
                                           message=message
                                           )
                articleId = main_2(url, type_str)
                return redirect(url_for('page.articleChar', articleId=articleId))
        except Exception as e:
            print(e)
            error_message = str(e)
            print(f"An unexpected error occurred: {error_message}")
            if error_message == 'You should supply an encoding or a list of encodings to this method that includes input_ids, but you provided []':
                return render_template('spiderData.html',
                                       username=username,
                                       message='地址错误'
                                       )
            return render_template('spiderData.html',
                                   username=username,
                                   message=error_message
                                   )

        return render_template('spiderData.html',
                               username=username,
                               message=message
                               )

    # 爬取多个文章
    @blueprint.route('/spiderArticles', methods=['GET'])
    def spiderArticles():
        from spiders.main import main as startSpider
        
        message = ''
        username = session.get('username')
        try:
            types = request.args.get('types')
            page = request.args.get('page')
            print("Selected types: {}, Selected page: {}".format(types, page))
            if page is not None:
                page = int(page)
            else:
                page = 1  # 默认值
            if types is not None:
                startSpider(types, page)
                message = '爬取成功'
                return redirect(url_for('page.articleData_temp'))
        except Exception as e:
            error_message = str(e)
            print(f"An unexpected error occurred: {error_message}")
            if error_message == 'You should supply an encoding or a list of encodings to this method that includes input_ids, but you provided []':
                return render_template('spiderData.html',
                                       username=username,
                                       message='文章类型太少或页数太少'
                                       )
            elif error_message.find('Expecting value: line') == 0:
                return render_template('spiderData.html',
                                       username=username,
                                       message='Cookie失效'
                                       )
            return render_template('spiderData.html',
                                   username=username,
                                   message=error_message
                                   )

        return render_template('spiderData.html',
                               username=username,
                               message=message
                               )

    @blueprint.route('/spiderData', methods=['GET'])
    def spiderData():
        username = session.get('username')
        return render_template('spiderData.html',
                               username=username
                               )

