import os

import pymysql
from pymysql import *
import pandas as pd

conn = connect(host='localhost', port=3306, user='root', password='Fjj2351482820', database='weiboarticles')
cursor = conn.cursor()


# 检查数据库连接
def check_connection():
    try:
        conn.ping(reconnect=True)
    except pymysql.MySQLError as e:
        print(f"数据库连接失败: {e}")
        raise


def delete_articles(article_ids):
    try:
        if isinstance(article_ids, int):
            article_ids = [article_ids]  # 将整数转换为列表
        sql_query = "DELETE FROM article WHERE id IN (%s)" % ','.join(['%s'] * len(article_ids))
        cursor.execute(sql_query, article_ids)
        sql_query = "DELETE FROM comments WHERE articleId IN (%s)" % ','.join(['%s'] * len(article_ids))
        cursor.execute(sql_query, article_ids)

        conn.commit()

        return True
    except Exception as e:
        print(f"Error deleting articles: {e}")
        conn.rollback()
        return False


def delete_all_articles():
    try:
        sql = "DELETE FROM article"
        cursor.execute(sql)

        sql = "DELETE FROM comments"
        cursor.execute(sql)

        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting all articles: {e}")
        conn.rollback()
        return False


def getAllArticleData():
    check_connection()
    try:
        sql = "SELECT * FROM article"
        cursor.execute(sql)
        articleList = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return articleList


def getAllArticleData_temp():
    check_connection()
    try:
        sql = "SELECT * FROM article_temp"
        cursor.execute(sql)
        articleList = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return articleList


def get_top_100_comments():
    check_connection()
    try:
        # 查询 likes_counts 排名前 100 的评论
        sql = """
            SELECT * FROM comments
            ORDER BY likes_counts DESC
            LIMIT 100
        """
        cursor.execute(sql)
        top_comments = cursor.fetchall()

        # 将结果转换为列表
        top_comments_list = [list(comment) for comment in top_comments]

        return top_comments_list
    except Exception as e:
        print(f"发生错误: {e}")
        return []
    finally:
        conn.close()


def getAllNegativeArticle():
    check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY negative_ratio DESC LIMIT 10"
        cursor.execute(sql)
        articleList = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return articleList


def getAllNeutralArticle():
    check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY neutral_ratio DESC LIMIT 10"
        cursor.execute(sql)
        articleList = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return articleList

def getAllPositiveArticle():
    check_connection()
    try:
        sql = "SELECT * FROM article ORDER BY positive_ratio DESC LIMIT 10"
        cursor.execute(sql)
        articleList = cursor.fetchall()
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return articleList


def getAllCommentsData():
    commentsList = query('select * from comments', [], 'select')
    return commentsList


def query(sql, params, query_type="no_select"):
    try:
        conn.ping(reconnect=True)  # 在查询前检查并保持连接
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            if query_type != 'no_select':
                data_list = cursor.fetchall()
                return data_list
            else:
                conn.commit()  # 提交事务以确保更改被保存
    except pymysql.err.InterfaceError:
        print("数据库连接已断开，尝试重新连接...")
        conn.ping(reconnect=True)
        return query(sql, params, query_type)
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()


def save_to_sql(articleDataFilePath, articleCommentsFilePath):
    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 批量插入文章数据
        articles_data = [tuple(row) for row in articlePd.values]
        article_sql = """
            INSERT INTO article (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [tuple(row) for row in commentPd.values]
        comment_sql = """
            INSERT INTO comments (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        cursor.executemany(comment_sql, comments_data)

        # 提交事务
        conn.commit()

        # 确保文件在数据成功保存后才删除
        # os.remove(articleDataFilePath)
        # os.remove(articleCommentsFilePath)

    except Exception as e:
        print(f"发生错误: {e}")
        conn.rollback()


# 存储临时数据
def save_to_sql_temp(articleDataFilePath, articleCommentsFilePath):
    try:
        sql = "DELETE FROM article_temp"
        cursor.execute(sql)

        sql = "DELETE FROM comments_temp"
        cursor.execute(sql)

        conn.commit()
    except Exception as e:
        print(f"Error deleting all articles: {e}")
        conn.rollback()
        return False

    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 批量插入文章数据
        articles_data = [tuple(row) for row in articlePd.values]
        article_sql = """
            INSERT INTO article_temp (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [tuple(row) for row in commentPd.values]
        comment_sql = """
            INSERT INTO comments_temp (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        cursor.executemany(comment_sql, comments_data)

        # 提交事务
        conn.commit()

        # 确保文件在数据成功保存后才删除
        # os.remove(articleDataFilePath)
        # os.remove(articleCommentsFilePath)

    except Exception as e:
        print(f"发生错误: {e}")
        conn.rollback()


# 保存一篇文章数据，爬取指定文章，更新文章。先查后存
def save_to_article(articleDataFilePath, articleCommentsFilePath, articleId):
    delete_articles(articleId)
    try:
        # 读取新的 CSV 数据
        articlePd = pd.read_csv(articleDataFilePath)
        commentPd = pd.read_csv(articleCommentsFilePath)

        # 2024.9.19更新代码=================================
        # 将 NaN 值替换为 None
        articlePd = articlePd.astype(object).where(pd.notnull(articlePd), None)
        commentPd = commentPd.astype(object).where(pd.notnull(commentPd), None)
        # 2024.9.19更新代码==================================

        # 批量插入文章数据
        articles_data = [tuple(row) for row in articlePd.values]
        article_sql = """
            INSERT INTO article (id,likeNum,commentsLen,reposts_count,region,content,created_at,type,detailUrl,authorName,authorDetail,
            negative_ratio,neutral_ratio,positive_ratio,emotion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(article_sql, articles_data)

        # 批量插入评论数据
        comments_data = [tuple(row) for row in commentPd.values]
        comment_sql = """
            INSERT INTO comments (articleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,sentiment)
            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s)
        """
        cursor.executemany(comment_sql, comments_data)

        # 提交事务
        conn.commit()

        # 确保文件在数据成功保存后才删除
        # os.remove(articleDataFilePath)
        # os.remove(articleCommentsFilePath)

    except Exception as e:
        print(f"发生错误: {e}")
        conn.rollback()


def getArticleData(id):
    return query('select * from article where id=%s',[id],'select')

def getCommentsData(id):
    if id is not None:
        commentsList=query('select * from comments where articleId=%s',[id],'select')
        commentsList = list(commentsList)
        commentsList.sort(key=lambda x: x[2],reverse=True)
        return commentsList
    return []

def getAllCommentsData():
    allCommentList = query('select * from comments',[],'select')
    return allCommentList

# save_to_article(r'C:\Users\81217\Desktop\weibo\spiders\data\articleContent_2024-09-17_23-34-55.csv',
#                 r'C:\Users\81217\Desktop\weibo\spiders\data\articleComments_2024-09-17_23-34-55.csv',
#                 5079635350000595)

def FindBySchoolName(schoolname):
    "该函数通过schoolname查找school表中所有该学校的评论"
    print("调用FindBySchoolname函数")
    
    check_connection()
    try:
        sql = "SELECT * FROM school WHERE school_name=%s"
        cursor.execute(sql, schoolname)
        schoolList = cursor.fetchall()
        
        school_list = [list(comment) for comment in schoolList]

        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    
    return school_list

def FindByCommentsId(id):
    "该函数通过评论id查找评论表中所有该评论的相关信息"
    print("调用FindByCommentsId函数")
    check_connection()
    try:
        sql = "SELECT * FROM school WHERE commentId=%s"
        cursor.execute(sql, id)
        commentsList = cursor.fetchall()
        comments_list = [list(comment) for comment in commentsList]
        conn.commit()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        conn.rollback()
        return []
    except Exception as e:
        print(f"其他错误: {e}")
        conn.rollback()
        return []
    return comments_list

# if __name__ == '__main__':
#     #FindBySchoolName("北京大学")
#     FindByCommentsId(1067921652)
