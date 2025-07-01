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


if __name__ == '__main__':
    # 登录测试
    print(login('1', '1'))
    # 注册测试
    print(register(3, '3'))
    # 注册测试
    print(register(5, '5'))

