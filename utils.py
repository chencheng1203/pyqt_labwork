# -*- encoding:utf-8 -*-
# @Time: 2020/1/7 9:40
import pymysql
import arrow
import docx
import datetime


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
    return data

# 插入记录数据
def insert_op_record(user, op_type):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "insert into op_record (user, op_type) values('{}', '{}');".format(user, op_type)
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 获取操作记录数据库数据
def get_op_record_all():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from op_record;"
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data

def get_op_record_time(beg, end):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from op_record where date(time) between '{}' and '{}';".format(beg, end)
    cursor.execute(sql)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return data


# 获取前 n 个月的时间
def get_n_month_time(n_month):
    dt = arrow.now()
    ttime = dt.shift(months=-n_month).format("YYYY-MM-DD HH:MM:SS")
    return ttime


# 删除前 n 个月的操作数据
def remove_n_month_data(n_month):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    month_time = get_n_month_time(n_month)
    if int(month_time[-2:]) >= 60:
        new_month_time = month_time[:-2] + "00"
    else:
        new_month_time = month_time
    sql = "delete from op_record where time<'{}';".format(new_month_time)
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 将71个关键词标题插入表单
def insert_data2keyword_dic_table():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    dic_path = r"D:\实验室项目相关文档\小开发\keyword_doc\keyword_dic.docx"
    d = docx.opendocx(dic_path)  # 打开数据
    doc = docx.getdocumenttext(d)
    for word in doc:
        sql = "insert into keyword_dic_table (keyword) values('{}');".format(word)
        cursor.execute(sql)
        conn.commit()
    conn.close()
    print("insert_data2keyword_dic_table done")


# 将71个关键词从表单中读取出来
def read_data_from_keyword_dic_table():
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from keyword_dic_table;"
    cursor.execute(sql)
    data_return = cursor.fetchall()
    data = []
    for i in data_return:
        for j in i:
            data.append(j)
    conn.commit()
    conn.close()
    return data


# 插入文件检查检查记录
def file_check_record_insert(check_id, ip, file_name, keyword_input, keyword, degree_selected):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "insert into file_check_record (check_id, ip, file_name, keyword_input, keyword, degree_selected) values('{}', '{}', '{}', '{}', '{}', '{}');"\
        .format(check_id, ip, file_name, keyword_input, keyword, degree_selected)
    cursor.execute(sql)
    conn.commit()
    conn.close()


# 返回文件检查置信度
def file_check_conf_return(keyword):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root", password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select COUNT(*) from file_check_record where keyword_input='{}'".format(keyword)
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    conn.close()
    return data[0][0]

if __name__ == "__main__":
    data = read_data_from_keyword_dic_table()
    print(data)