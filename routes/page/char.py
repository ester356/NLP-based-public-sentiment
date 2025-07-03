
from flask import session, render_template, request
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_char_routes(blueprint):
    @blueprint.route('/yuqingChar')
    def yuqingChar():
        from utils.base_page import getAllNegativeArticle, getAllNeutralArticle, getAllPositiveArticle
        
        username = session.get('username')
        negative_articleList = getAllNegativeArticle()
        neutral_articleList = getAllNeutralArticle()
        positive_articleList = getAllPositiveArticle()
        return render_template('yuqingChar.html',
                               username=username,
                               negative_articleList=negative_articleList,
                               neutral_articleList=neutral_articleList,
                               positive_articleList=positive_articleList
                               )

    @blueprint.route('/articleChar', methods=['GET'])
    def articleChar():
        from utils.base_page import (getArticleID, getTypeList, getCommentsData, 
                                   getArticleData, getIPCharByCommentsRegion, 
                                   getCommentSentimentData, getTimeData)
        
        username = session.get('username')
        articleIDList = getArticleID()
        typeList = getTypeList()
        if articleIDList:
            defaultArticleID = articleIDList[0]
        else:
            defaultArticleID = None  
        if request.args.get('articleId'): 
            defaultArticleID = request.args.get('articleId')
        commentsList = getCommentsData(str(defaultArticleID))
        article = getArticleData(str(defaultArticleID))
        commentRegionData = getIPCharByCommentsRegion(commentsList)
        sentimentData = getCommentSentimentData(commentsList)
        time_dates, time_counts = getTimeData(commentsList)
        return render_template('articleChar.html',
                               username=username,
                               articleIDList=articleIDList,
                               typeList=typeList,
                               defaultArticleID=defaultArticleID,
                               likeNum=article[0][1],
                               commentsLen=article[0][2],
                               reposts_count=article[0][3],
                               region=article[0][4],
                               content=article[0][5],
                               created_at=article[0][6],
                               type=article[0][7],
                               detailUrl=article[0][8],
                               authorName=article[0][9],
                               authorDetail=article[0][10],
                               commentsList=commentsList,
                               sentimentData=sentimentData,
                               commentRegionData=commentRegionData,
                               time_dates=time_dates,
                               time_counts=time_counts
                               )
