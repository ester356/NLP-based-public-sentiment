
from flask import session, render_template, request
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_analyse_routes(blueprint):
    @blueprint.route('/analysisTopic')
    def analysisTopic():
        from utils.topicAnalysis import getWeiboAI, generate_wordcloud, getCharData, getCiTiaoList
        
        username = session.get('username')
        try:
            ciTiao = request.args.get('ciTiao')
            description_list, emotion, word_cloud, typical_viewpoint_list = getWeiboAI(ciTiao)
            generate_wordcloud(word_cloud, ciTiao)
            names, nums = getCharData(emotion)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            message = "暂无分析结果，请重新选择话题"
            ciTiaoList = getCiTiaoList()
            return render_template('topic.html',
                                   username=username,
                                   message=message,
                                   ciTiaoList1=ciTiaoList[:10],
                                   ciTiaoList2=ciTiaoList[10:]
                                   )
        return render_template('analysisTopic.html',
                               username=username,
                               description_list=description_list[:5],
                               emotion=json.dumps(emotion),
                               names=names,
                               nums=nums,
                               ciTiao=ciTiao,
                               typical_viewpoint_list=typical_viewpoint_list[:10]
                               )

    @blueprint.route('/SchoolAnalyse')
    def ScoolAnalyse():
        from utils.schoolAnalysis import analysis_school
        
        username = session.get('username')
        school_name = request.args.get('school_name')
        try:
            # 调用分析函数
            school_data = analysis_school(school_name)
        except Exception as e:
            print(f"学校分析失败: {e}")
            school_data = []

        # 假设你已经获取了三个情感的数量
        positive = sum(1 for c in school_data if c['emotion'] == '积极')
        neutral = sum(1 for c in school_data if c['emotion'] == '中性')
        negative = sum(1 for c in school_data if c['emotion'] == '消极')
        total = positive + neutral + negative

        # 避免除以0
        positive_ratio = round(positive / total * 100, 1) if total else 0
        neutral_ratio = round(neutral / total * 100, 1) if total else 0
        negative_ratio = 100 - positive_ratio - neutral_ratio  # 确保加起来是100

        return render_template('SchoolAnalyse.html', 
                               username=username, 
                               School_Comments=school_data,
                               positive_ratio=positive_ratio,
                               neutral_ratio=neutral_ratio,
                               negative_ratio=negative_ratio,
                               School_Comments_graph=school_data
                               )
