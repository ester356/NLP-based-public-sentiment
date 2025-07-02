import pymysql
from pymysql import connect
import datetime
import user_db_manage 
# === 建立数据库连接 ===
conn = connect(
    host='localhost',
    port=3306,
    user='root',
    password='Ljj200402260522',
    database='weiboarticles',
    charset='utf8mb4'
)
cursor = conn.cursor()

# === 数据库操作 ===
def check_connection():
    """
    检查并保持数据库连接
    """
    try:
        conn.ping(reconnect=True)
    except pymysql.MySQLError as e:
        print(f"[连接错误] 数据库连接失败: {e}")
        raise
#-----------------------------------------------------------------管理员的登录和注册功能----------------------------------------------------
def login(id, password):
    """
    登录函数：验证用户名和密码是否匹配
    :param ID: 用户ID
    :param password: 密码
    :return: True 表示登录成功，False 表示失败
    """
    try:
        check_connection()
        sql = "SELECT * FROM user WHERE ID=%s AND password=%s"
        cursor.execute(sql, (id, password))
        result = cursor.fetchone()
        return result is not None
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 登录失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 登录失败: {e}")
        conn.rollback()
        return False

def register(id, password):

    """
    注册函数：将新管理员插入 admin 表
    :param id: 管理员ID (int)
    :param password: 密码 (字符串) 
    :return: True 表示注册成功，False 表示失败（如管理员已存在） 
    注意：系统只能有四位管理员 要求id分别为  1 2 3 4
    """ 
    try:
        check_connection()
        #获取当前的时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if id not in ['1', '2', '3', '4',1,2,3,4]:
            print(f"[注册失败] 管理员ID只能为 1 2 3 4")
            return False
        sql = "INSERT INTO admin (id, password,create_time) VALUES (%s, %s,%s)"
        cursor.execute(sql, (id, password,now))
        conn.commit()
        return True
    except pymysql.IntegrityError as e:
        print(f"[注册失败] 用户名已存在或违反唯一性约束: {e}")
        conn.rollback()
        return False
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 注册失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 注册失败: {e}")
        conn.rollback()
        return False
    
#------------------------------------------对用户的增删改查（1号管理员）---------------------------------------------------------    
def add_user(user_id,password,permission,admin_id):
    '''
     添加用户函数：能增加用户
     参数：用户ID,用户密码，用户权限，管理员ID
    '''
    try:
        admin_id = int(admin_id)
        if admin_id == 1:
            check_connection()
            #获取当前的时间
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO user (id, password,create_time,permission,admi_id) VALUES (%s, %s,%s,%s,%s)"
            cursor.execute(sql, (user_id, password,now,permission,admin_id)) #
            conn.commit()
            return True
        else:
            print(f"[用户增加失败]，用户的增加只能由1号管理员实现")
            return False
    except pymysql.IntegrityError as e:
        print(f"[用户增加失败] 用户名已存在或违反唯一性约束: {e}")
        conn.rollback()
        return False
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 用户增加失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 用户增加失败: {e}")
        conn.rollback()
        return False
def delete_user(user_id,admin_id):
    '''
     删除用户函数：能删除用户
     参数：用户ID 管理员ID
    '''
    try:
        admin_id = int(admin_id)
        if admin_id == 1:
            check_connection()
            #先查看Id是否存在
            sql = "SELECT * FROM user WHERE id = %s"
            if cursor.execute(sql, (user_id)) == 0:
                print(f"[用户删除失败]，用户ID不存在")
                return False
            #删除指定ID的用户
            sql = "DELETE FROM user WHERE id = %s"
            cursor.execute(sql, (user_id,))
            conn.commit()
            return True
        else:
            print(f"[用户删除失败]，用户的删除只能由1号管理员实现")
            return False
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 用户删除失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 用户删除失败: {e}")
        conn.rollback()
        return False
    
def change_user_permission(user_id,new_permission,admin_id):
    '''
     修改用户权限函数：能修改用户的权限
     参数：用户ID 修改后的权限 管理员ID
    '''
    try:
        admin_id = int(admin_id)
        if admin_id == 1:
            check_connection()
            #先查看Id是否存在
            sql = "SELECT * FROM user WHERE id = %s"
            if cursor.execute(sql, (user_id)) == 0:
                print(f"[用户权限修改失败]，用户ID不存在")
                return False
            #修改指定ID的用户的权限 
            sql = "UPDATE user SET permission = %s WHERE id = %s"
            cursor.execute(sql, (new_permission, user_id))
            conn.commit()
            return True
        else:
            print(f"[用户权限修改失败]，用户的权限修改只能由1号管理员实现")
            return False
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 用户权限修改失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 用户权限修改失败: {e}")
        conn.rollback()
        return False

#对用户的查询操作暂时先不写

#---------------------------------------------对文章的操作（2）号管理员-------------------------------------------

#暂时不用增加文章



#删除文章 
def delete_article(article_id,admin_id):
    '''
     删除文章函数：能删除指定ID的文章 只有2号管理员可以操作
     参数：文章ID 管理员ID
     '''
    try:
        admin_id = int(admin_id)
        if admin_id == 2:
            check_connection()
            #先查看Id是否存在
            sql = "SELECT * FROM article WHERE id = %s"
            if cursor.execute(sql, (article_id)) == 0:
                print(f"[文章删除失败]，文章ID不存在")
                return False
            #删除指定ID的文章
            sql = "DELETE FROM article WHERE id = %s"
            cursor.execute(sql, (article_id,))
            conn.commit()
            return True
        else:
            print(f"[文章删除失败]，文章的删除只能由2号管理员实现")
            return False
    except pymysql.MySQLError as e:
        print(f"[数据库错误] 文章删除失败: {e}")
        conn.rollback()
        return False
    except Exception as e:
        print(f"[其他错误] 文章删除失败: {e}")
        conn.rollback()
        return False

#修改文章：


#查询文章：


#---------------------------------------------对评论的操作（3）号管理员-------------------------------------------







#---------------------------------------------对日记和舆情分析记录的查看（4）号管理员-------------------------------------------








if __name__ == '__main__':


#------------------------------------------管理员登录注册功能-----------------------------------------------------
    '''
    # 登录测试
    print(login('1', '1'))
    # 注册测试
    print(register(3, '3'))
    # 注册测试
    print(register(5, '5'))
    '''


#--------------------------------------------------对用户的增删改查操作（1）号管理员---------------------------------
    # 添加用户测试
    print(add_user(6, '6', '1', 1))

    # 删除用户测试
    print(delete_user(6, '1'))
    
    #修改用户的权限
    print(change_user_permission('1',1,1))

    #查看用户 暂时不写
#-----------------------------------------------------对文章的操作（2）号管理员-----------------------------------------
    print(delete_article(5062309233296726,2))
