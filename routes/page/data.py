
from flask import session, render_template, request
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_data_routes(blueprint):
    @blueprint.route('/commentsData')
    def commentsData():
        from utils.base_page import get_top_100_comments
        
        username = session.get('username')
        top_comments_list = get_top_100_comments()
        if top_comments_list:
            print(top_comments_list[0])
        else:
            print("Warning: top_comments_list is empty!")
        return render_template('commentsData.html',
                               username=username,
                               top_comments_list=top_comments_list
                               )

    @blueprint.route('/articleData_temp', methods=['GET'])
    def articleData_temp():
        from utils.base_page import getAllArticleData_temp
        
        username = session.get('username')
        articeList = getAllArticleData_temp()
        return render_template('articleData_temp.html',
                               username=username,
                               articeList=articeList
                               )

    @blueprint.route('/topic')
    def topic():
        from utils.topicAnalysis import getCiTiaoList
        
        username = session.get('username')
        try:
            ciTiaoList = getCiTiaoList()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            ciTiaoList = []
        return render_template('topic.html',
                               username=username,
                               ciTiaoList1=ciTiaoList[:10] if len(ciTiaoList) > 10 else ciTiaoList,
                               ciTiaoList2=ciTiaoList[10:] if len(ciTiaoList) > 10 else []
                               )

    @blueprint.route('/updateData')
    def updateData():
        from utils.base_page import getAllArticleData
        
        username = session.get('username')
        articeList = getAllArticleData()
        return render_template('updateData.html',
                               username=username,
                               articeList=articeList
                               )

    @blueprint.route('/articleData')
    def tableData():
        from utils.base_page import getAllArticleData
        
        username = session.get('username')
        articeList = getAllArticleData()
        return render_template('articleData.html',
                               username=username,
                               articeList=articeList
                               )


