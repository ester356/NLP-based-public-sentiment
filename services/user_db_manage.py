import pymysql
from pymysql import connect
import datetime

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


def check_connection():
    """
    检查并保持数据库连接
    """
    try:
        conn.ping(reconnect=True)
    except pymysql.MySQLError as e:
        print(f"[连接错误] 数据库连接失败: {e}")
        raise


def login(id, password):
    """
    登录函数：验证用户名和密码是否匹配
    :param username: 用户名
    :param password: 密码
    :return: True 表示登录成功，False 表示失败
    """
    try:
        check_connection()
        sql = "SELECT * FROM user WHERE id=%s AND password=%s"
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
def register(username, password):
    """
    注册函数：将新用户插入 user 表
    :param username: 用户名
    :param password: 密码
    :return: True 表示注册成功，False 表示失败（如用户名已存在）
    """
    try:
        check_connection()
        #获取当前的时间
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO user (id, password,create_time,permission,admi_id) VALUES (%s, %s,%s,%s,%s)"
        cursor.execute(sql, (username, password,now,0,1)) #默认权限为0，管理员id为1
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


# ===== 测试代码区 =====
if __name__ == '__main__':
    id = '1'
    password = '1'
    
    
    if login(id, password):
        print("登录成功")
    else:
        print("登录失败，用户名或密码错误")
