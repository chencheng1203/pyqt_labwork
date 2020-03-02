# -*- encoding:utf-8 -*-
# @Time: 2020/1/7 9:40
import pymysql


# 获取当前时间
def get_current_time():
    import time
    returned_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return returned_time


# 插入数据
def insert_user(username, pw):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    # 定义插入语句
    insert_sql = "insert into user_account(user_name, passwd) values('{}','{}');".format(username, pw)
    try:
        flag = cursor.execute(insert_sql)
        conn.commit()
    except:
        print("用户名存在")
        return 0
    # 关闭数据库
    cursor.close()
    conn.close()
    return 1


# 遍历用户数据库
def search_all_user_account():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    search_all_user_account_sql = "select * from user_account"
    cursor.execute(search_all_user_account_sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# 查找用户是否存在
def search_user(username, pd):
    # 第一个返回用户是否存在，第二个返回密码是否正确
    return_data = [0, 0]
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    user_search_sql = "select * from user_account where user_name='{}'".format(username)
    pw_search_sql = "select * from user_account where user_name='{}' and passwd='{}'".format(username, pd)
    cursor.execute(user_search_sql)
    data = cursor.fetchall()
    if len(data) != 0:
        return_data[0] = 1
    else:
        return_data[0] = 0
    cursor.execute(pw_search_sql)
    data = cursor.fetchall()
    if len(data) != 0:
        return_data[1] = 1
    else:
        return_data[1] = 0
    return return_data


# 数据库配置-保存配置处理函数
def database_config_save_data(check_person, checked_company):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "insert into database_config (check_person, checked_company) values('{}','{}');".format(check_person, checked_company)
    flag = cursor.execute(sql)
    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()
    return flag


# 查看数据
def show_data(keyword):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from {}".format(keyword)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# 将关键词保存到关键词库
def save_keyword_to_keyword_lib(kw, keyword_lib):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "insert into {}(keyword) values('{}');".format(keyword_lib, kw)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# 查询所有用户
def display_user_account():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from user_account;"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data;


if __name__ == "__main__":
    print(display_user_account())