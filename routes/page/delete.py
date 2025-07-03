
from flask import session, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_delete_routes(blueprint):
    @blueprint.route('/delete_all_articles', methods=['POST'])
    def delete_all_articles_route():
        from utils.base_page import delete_all_articles
        
        try:
            if delete_all_articles():
                return jsonify({'status': 'success', 'message': '所有文章成功删除'})
            else:
                return jsonify({'status': 'failure', 'message': '删除失败'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @blueprint.route('/delete_articles', methods=['POST'])
    def delete_articles_route():
        from utils.base_page import delete_articles
        
        try:
            data = request.get_json()
            article_ids = data.get('articleIds', [])
            if delete_articles(article_ids):
                return jsonify({'status': 'success', 'message': '文章成功删除'})
            else:
                return jsonify({'status': 'failure', 'message': '文章删除失败'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

    @blueprint.route('/deleteData')
    def deleteData():
        from utils.base_page import getAllArticleData
        
        username = session.get('username')
        articeList = getAllArticleData()
        return render_template('deleteData.html',
                               username=username,
                               articeList=articeList
                               )
