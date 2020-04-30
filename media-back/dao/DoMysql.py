import pymysql


# 这里可以通过配置文件或者传参的方式来封装，但是我们用配置文件比较好管理
# 加载数据库
def init_db():
    dbhost = '120.26.106.222'
    dbuser = 'julai01'
    passwd = 'Sh51785136@sh'
    dbname = 'jijin'
    mysql = pymysql.connect(dbhost, dbuser, passwd, dbname, charset='utf8')
    # 2.新建个查询页面
    cursor = mysql.cursor()
    return cursor,mysql
# 加载test库
def init_test_db():
    dbhost = '120.26.106.222'
    dbuser = 'julai01'
    passwd = 'Sh51785136@sh'
    dbname = 'test'
    mysql = pymysql.connect(dbhost, dbuser, passwd, dbname, charset='utf8')
    # 2.新建个查询页面
    cursor = mysql.cursor()
    return cursor,mysql

# 返回jijin库单条数据
def fetch_one(sql):
    result=init_db()
    result[0].execute(sql)
    result[0].close()
    result[1].close  ()
    return result[0].fetchone()

# 返回jijin库多条数据
def fetch_chall(sql):
    result=init_db()
    result[0].execute(sql)
    result[0].close()
    result[1].close()
    return result[0].fetchall()
# 执行test库增删改操作
def commit_chall_test(sql):
    result=init_test_db()
    result[0].execute(sql)
    result[1].commit()
    result[0].close()
    result[1].close()
    return 1
# 返回test库单条数据
def fetch_one_test(sql):
    result=init_test_db()
    result[0].execute(sql)
    result[0].close()
    result[1].close()
    return result[0].fetchone()
# 返回test库多条数据
def fetch_chall_test(sql):
    result=init_test_db()
    result[0].execute(sql)
    result[0].close()
    result[1].close()
    return result[0].fetchall()
