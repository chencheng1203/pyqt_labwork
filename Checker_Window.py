# -*- encoding:utf-8 -*-
# @Time: 2020/2/26 8:16

# -*- encoding:utf-8 -*-
# @Time: 2020/1/1 15:02

import sys
import docx
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QCheckBox, \
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QProgressBar,\
    QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QAbstractItemView, \
    QDesktopWidget, QStackedWidget, QComboBox, QHeaderView, QCalendarWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
from info_dialog import user_already_exist
from utils import database_config_save_data, save_keyword_to_keyword_lib, show_data, save_keyword_to_keyword_lib,\
    display_user_account, get_op_record_all, get_op_record_time, remove_n_month_data, read_data_from_keyword_dic_table

# 创建关键词库字典
doc = read_data_from_keyword_dic_table()
keyword_title_dic = {}
for i, keyword in enumerate(doc):
    keyword_title_dic["keyword" + str(i + 1)] = keyword

# 一开始显示的内容
ori_show_data_context = ""
data = show_data("keyword" + str(1))
for keyword_pair in data:
    ori_show_data_context += (keyword_pair[1] + " ")


class Checker_Win(QWidget):
    def __init__(self):
        super(Checker_Win, self).__init__()

        # 右侧控件设置
        self.stack_user_account_manager = QWidget()  # 账号管理
        self.stack_shenjin_manager = QWidget()  # 审计管理
        self.stack_rizhi_delete = QWidget()  # 日志清理

        # 数据表check记录
        self.delete_check = []

        # 提示窗口初始化
        self.user_already_exist_win = user_already_exist()

        self.initUI()  # 基本信息初始化
        self.initLayout()  # 布局初始化

    def initUI(self):
        self.setWindowTitle('数据库检查系统')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"D:\Code\PyQt\bupt_prj01\images/软件图标.ico"))
        self.resize(1200, 800)
        self.center()
        self.setFixedSize(self.width(), self.height())

        # 设置窗口样式
        win_palette = QPalette()  # 设置窗口样式
        win_palette.setBrush(QPalette.Background, QBrush(QPixmap(r'D:\Code\PyQt\bupt_prj01\images/bg3.jpg')))
        self.setPalette(win_palette)

        # 大标题
        self.title_layout = QHBoxLayout()
        title_image_label = QLabel(self)
        title_label = QLabel("数据库检查系统")
        title_label.setFont(QFont('Ink Free', 22, QFont.Bold))
        title_image_label.setPixmap(QPixmap(r'D:\Code\PyQt\bupt_prj01\images\数据库维护服务.png'))
        # title_image_label.setMaximumSize(50, 50)
        self.title_layout.addStretch(1)
        self.title_layout.addWidget(title_image_label)
        self.title_layout.addWidget(title_label)
        self.title_layout.addStretch(1)

        # 信息栏
        self.info_box = QLineEdit(self)
        self.info_box.setReadOnly(True)  # 设置为只读
        self.info_box.setAlignment(Qt.AlignCenter)
        self.info_box.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.info_box.setFixedHeight(30)
        self.info_box_layout = QHBoxLayout()
        self.info_box_layout.setContentsMargins(0, 0, 0, 0)
        self.info_box_layout.addWidget(self.info_box)
        # 设置信息栏信息
        self.Timer = QTimer()
        self.Timer.start(500)
        self.Timer.timeout.connect(self.updateTime)

        # 系统导航标签
        sys_guide_label = QLabel("系统导航", self)
        sys_guide_label.setStyleSheet("color:white")
        sys_guide_label.setFont(QFont('Microsoft YaHei', 15))
        self.sys_guide_layout = QHBoxLayout()
        self.sys_guide_layout.addSpacing(25)
        self.sys_guide_layout.addWidget(sys_guide_label)

        # 左侧导航栏
        # 加载样式
        with open(r'D:\Code\PyQt\bupt_prj01\QListWidgetQSS.qss', 'r') as f:
            qssStyle = f.read()

        self.func_menu = QListWidget()
        self.func_menu.setStyleSheet(qssStyle)
        self.func_menu.setFrameShape(QListWidget.NoFrame)  # 去掉边框
        list_items = ['账号管理', '审计管理', '日志清除']
        for i in range(len(list_items)):
            self.item = QListWidgetItem(list_items[i], self.func_menu)
            self.item.setSizeHint(QSize(25, 207))
            self.item.setTextAlignment(Qt.AlignCenter)
            # func_menu.insertItem(i, list_items[i])
        self.func_menu.currentRowChanged.connect(self.stack_UI_display)  # 连接信号

        # 右侧控件设置
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_user_account_manager)
        self.Stack.addWidget(self.stack_shenjin_manager)
        self.Stack.addWidget(self.stack_rizhi_delete)


        self.main_menu_layout = QHBoxLayout()
        self.main_menu_layout.addWidget(self.func_menu)
        self.main_menu_layout.addWidget(self.Stack)

        self.stack_user_account_manager_UI()
        self.stack_shenjin_manager_UI()
        self.stack_rizhi_delete_UI()

        # self.mian_menu_layout.addSpacing(1000)

    # 用户管理
    def stack_user_account_manager_UI(self):
        # 是否增加用户
        if_add_user_layout = QHBoxLayout()
        if_add_user_label = QLabel("是否增加用户")
        if_add_user_label.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_user_YES_choose = QRadioButton("是")
        self.if_add_user_YES_choose.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_user_NO_choose = QRadioButton("否")
        self.if_add_user_NO_choose.setChecked(True)  # 默认不选中
        self.if_add_user_NO_choose.setFont(QFont('Microsoft YaHei', 15))
        if_add_user_layout.addSpacing(30)
        if_add_user_layout.addWidget(if_add_user_label)
        if_add_user_layout.addSpacing(150)
        if_add_user_layout.addWidget(self.if_add_user_YES_choose)
        if_add_user_layout.addWidget(self.if_add_user_NO_choose)
        if_add_user_layout.addSpacing(160)

        # 用户名
        add_user_username_layout = QHBoxLayout()
        add_user_username_label = QLabel("用户名")
        add_user_username_label.setFont(QFont('Microsoft YaHei', 15))
        self.add_user_username_edit = QLineEdit()
        self.add_user_username_edit.setFixedWidth(600)
        self.add_user_username_edit.setFixedHeight(40)
        add_user_username_layout.addSpacing(55)
        add_user_username_layout.addWidget(add_user_username_label)
        add_user_username_layout.addSpacing(30)
        add_user_username_layout.addWidget(self.add_user_username_edit)
        add_user_username_layout.addSpacing(155)

        # 密码
        add_user_passwd_layout = QHBoxLayout()
        add_user_passwd_label = QLabel("密码")
        add_user_passwd_label.setFont(QFont('Microsoft YaHei', 15))
        self.add_user_passwd_edit = QLineEdit()
        self.add_user_passwd_edit.setFixedWidth(600)
        self.add_user_passwd_edit.setFixedHeight(40)
        add_user_passwd_layout.addSpacing(70)
        add_user_passwd_layout.addWidget(add_user_passwd_label)
        add_user_passwd_layout.addSpacing(70)
        add_user_passwd_layout.addWidget(self.add_user_passwd_edit)
        add_user_passwd_layout.addSpacing(160)

        # 添加用户按钮
        add_user_btn_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("添加用户")
        self.add_user_btn.clicked.connect(self.add_user)  # 槽函数
        self.add_user_btn.setFixedHeight(50)
        self.add_user_btn.setFixedWidth(900)
        self.add_user_btn.setProperty('name', 'add_user_btn')  # 设置按钮属性
        add_user_btn_qss = '''QPushButton[name='add_user_btn']{background-color:rgb(0,255,0)}'''
        self.add_user_btn.setFont(QFont('Microsoft YaHei', 15))
        self.add_user_btn.setStyleSheet(add_user_btn_qss)
        add_user_btn_layout.addWidget(self.add_user_btn)

        # 用户信息标签
        user_info_lable_layout = QHBoxLayout()
        user_info_lable_layout.setContentsMargins(0, 0, 0, 0)
        user_info_lable = QLabel('用户信息')
        user_info_lable.setFont(QFont('Microsoft YaHei', 15))
        user_info_lable_layout.addStretch(1)
        user_info_lable_layout.addWidget(user_info_lable)
        user_info_lable_layout.addStretch(1)

        # 用户信息表格
        user_info_table_layout = QHBoxLayout()
        user_info_table_layout.setContentsMargins(0, 0, 0, 0)
        self.delete_user_btn = QPushButton("删除")
        self.delete_user_btn.clicked.connect(self.delete_user)
        self.delete_user_btn.setFixedHeight(150)
        self.delete_user_btn.setFixedWidth(100)
        self.delete_user_btn.setProperty('name', 'delete_user_btn')
        delete_user_btn_qss = '''QPushButton[name='delete_user_btn']{background-color:rgb(255,0,0)}'''
        self.delete_user_btn.setStyleSheet(delete_user_btn_qss)
        self.user_info_table = QTableWidget()
        self.user_info_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.user_info_table.verticalHeader().hide()  # 隐藏行头
        self.user_info_table.setColumnCount(3)
        self.user_info_table.setHorizontalHeaderLabels(["用户名", "密码", "是否删除"])  # 设置表头
        self.user_info_table.setColumnWidth(0, 300)
        self.user_info_table.setColumnWidth(1, 300)
        self.user_info_table.setColumnWidth(2, 240)
        self.add_data_to_table()
        self.user_info_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        user_info_table_layout.addWidget(self.user_info_table)
        user_info_table_layout.addWidget(self.delete_user_btn)

        # 总体布局管理
        stack_user_manager_w1 = QWidget()
        stack_user_manager_w2 = QWidget()
        stack_user_manager_w3 = QWidget()
        stack_user_manager_w4 = QWidget()
        stack_user_manager_w5 = QWidget()
        stack_user_manager_w6 = QWidget()

        stack_user_manager_w1.setLayout(if_add_user_layout)
        stack_user_manager_w2.setLayout(add_user_username_layout)
        stack_user_manager_w3.setLayout(add_user_passwd_layout)
        stack_user_manager_w4.setLayout(add_user_btn_layout)
        stack_user_manager_w5.setLayout(user_info_lable_layout)
        stack_user_manager_w6.setLayout(user_info_table_layout)

        stack_user_manager_layout = QVBoxLayout()
        stack_user_manager_layout.addWidget(stack_user_manager_w1)
        stack_user_manager_layout.addWidget(stack_user_manager_w2)
        stack_user_manager_layout.addWidget(stack_user_manager_w3)
        stack_user_manager_layout.addWidget(stack_user_manager_w4)
        stack_user_manager_layout.addWidget(stack_user_manager_w5)
        stack_user_manager_layout.addWidget(stack_user_manager_w6)

        self.stack_user_account_manager.setLayout(stack_user_manager_layout)

    # 表格增加一行数据
    def add_line(self, user, passwd):
        row = self.user_info_table.rowCount()
        self.user_info_table.setRowCount(row + 1)
        # 下面六行用于生成居中的checkbox，不知道有没有别的好方法
        ck = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        self.user_info_table.setItem(row, 0, QTableWidgetItem(user))
        self.user_info_table.setItem(row, 1, QTableWidgetItem(passwd))
        self.user_info_table.setCellWidget(row, 2, w)
        self.delete_check.append(ck)
        self.update()

    # 添加用户
    def add_user(self):
        if self.if_add_user_YES_choose.isChecked():
            conn = pymysql.connect(
                host="127.0.0.1",
                user="root", password="cc120323",
                database="info_manager_sys",
                charset="utf8")
            cursor = conn.cursor()
            username = str(self.add_user_username_edit.text()).strip()
            pw = str(self.add_user_passwd_edit.text()).strip()
            if username != "" and pw != "":
                users = []
                for user, _ in display_user_account():
                    users.append(user)
                if username in users:
                    self.user_already_exist_win.show()
                else:
                    print(username)
                    print(pw)
                    sql = "insert into user_account(user_name, passwd) values('{}', '{}'); ".format(username, pw)
                    cursor.execute(sql)
                    conn.commit()
                    # 更新显示
                    self.add_data_to_table()

    # 增加多行数据
    def add_data_to_table(self):
        # 清空数据
        self.delete_check = []
        self.user_info_table.setRowCount(0)  # 清空数据
        datas = display_user_account()
        for data in datas:
            self.add_line(data[0], data[1])

    # 删除用户
    def delete_user(self):
        datas = display_user_account()
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root", password="cc120323",
            database="info_manager_sys",
            charset="utf8")
        cursor = conn.cursor()
        for i, line_check in enumerate(self.delete_check):
            if line_check.isChecked():  # 如果被选中
                delete_sql = "delete from user_account where user_name='{}'".format(datas[i][0])
                cursor.execute(delete_sql)
                conn.commit()  # 提交操作
        # 更新显示
        self.add_data_to_table()


    # 审计管理
    def stack_shenjin_manager_UI(self):
        # 查询类别
        search_method_layout = QHBoxLayout()
        search_method_layout.setContentsMargins(5, 5, 5, 5)
        search_method_label = QLabel("查询类别")
        search_method_label.setFont(QFont('Microsoft YaHei', 15))
        self.quanbu_choose = QRadioButton("全部")
        self.quanbu_choose.setChecked(True)
        self.quanbu_choose.toggled.connect(self.quanbu_choose_handle)
        self.quanbu_choose.setFont(QFont('Microsoft YaHei', 15))
        self.shijian_choose = QRadioButton("按时间")
        self.shijian_choose.toggled.connect(self.shijian_choose_handle)
        self.shijian_choose.setFont(QFont('Microsoft YaHei', 15))
        search_method_layout.addSpacing(80)
        search_method_layout.addWidget(search_method_label)
        search_method_layout.addSpacing(100)
        search_method_layout.addWidget(self.quanbu_choose)
        search_method_layout.addWidget(self.shijian_choose)
        search_method_layout.addSpacing(150)

        # 按照分类
        # search_on_class_layout = QHBoxLayout()
        # search_on_class_layout.setContentsMargins(5, 5, 5, 5)
        # search_on_class_label = QLabel('按照分类')
        # search_on_class_label.setFont(QFont('Microsoft YaHei', 15))
        # self.search_on_class_combox = QComboBox()
        # self.search_on_class_combox.currentIndexChanged.connect(self.search_on_class_index)
        # self.search_on_class_combox.addItems(["文件", "图片", "邮件"])
        # self.search_on_class_combox.setFixedHeight(40)
        # self.search_on_class_combox.setFixedWidth(450)
        # search_on_class_layout.addSpacing(80)
        # search_on_class_layout.addWidget(search_on_class_label)
        # search_on_class_layout.addSpacing(50)
        # search_on_class_layout.addWidget(self.search_on_class_combox)
        # search_on_class_layout.addSpacing(170)

        # 按照时间查询
        self.beg_cal = QCalendarWidget()
        self.beg_cal.clicked[QDate].connect(self.beg_cal_set)
        self.beg_cal.setGridVisible(True)
        self.end_cal = QCalendarWidget()
        self.end_cal.clicked[QDate].connect(self.end_cal_set)
        self.end_cal.setGridVisible(True)
        self.beg_cal.hide()
        self.end_cal.hide()

        search_on_time_layout = QHBoxLayout()
        search_on_time_layout.setContentsMargins(5, 5, 5, 5)
        search_on_time_label = QLabel('按照时间')
        search_on_time_label.setFont(QFont('Microsoft YaHei', 15))
        self.search_on_time_beg_btn = QPushButton("选择开始时间")
        self.search_on_time_beg_btn.setFixedWidth(100)
        self.search_on_time_beg_btn.clicked.connect(self.search_on_time_beg_btn_handle)
        self.search_on_time_end_btn = QPushButton("选择结束时间")
        self.search_on_time_end_btn.setFixedWidth(100)
        self.search_on_time_end_btn.clicked.connect(self.search_on_time_end_btn_handle)
        search_on_time_layout.addSpacing(80)
        search_on_time_layout.addWidget(search_on_time_label)
        search_on_time_layout.addWidget(self.search_on_time_beg_btn)
        search_on_time_layout.addSpacing(100)
        search_on_time_layout.addWidget(self.search_on_time_end_btn)
        search_on_time_layout.addSpacing(260)

        # 按照关键词
        # search_on_keyword_layout = QHBoxLayout()
        # search_on_keyword_layout.setContentsMargins(5, 5, 5, 5)
        # search_on_keyword_label = QLabel('输入关键词')
        # search_on_keyword_label.setFont(QFont('Microsoft YaHei', 15))
        # self.search_on_keyword_edit = QLineEdit()
        # self.search_on_keyword_edit.setFixedHeight(40)
        # self.search_on_keyword_edit.setFixedWidth(450)
        # search_on_keyword_layout.addSpacing(80)
        # search_on_keyword_layout.addWidget(search_on_keyword_label)
        # search_on_keyword_layout.addWidget(self.search_on_keyword_edit)
        # search_on_keyword_layout.addSpacing(170)

        # 开始查询按钮
        rizhi_start_search_btn_layout = QHBoxLayout()
        # start_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.rizhi_start_search_btn = QPushButton('开始查询')
        self.rizhi_start_search_btn.clicked.connect(self.add_data_to_op_table)
        self.rizhi_start_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.rizhi_start_search_btn.setFixedHeight(50)
        rizhi_start_search_btn_layout.addWidget(self.rizhi_start_search_btn)

        # 查询结果
        search_result_lable_layout = QHBoxLayout()
        search_result_lable_layout.setContentsMargins(5, 5, 5, 5)
        self.search_result_lable = QLabel('查询结果')
        self.search_result_lable.setFont(QFont('Microsoft YaHei', 15))
        search_result_lable_layout.addStretch(1)
        search_result_lable_layout.addWidget(self.search_result_lable)
        search_result_lable_layout.addStretch(1)

        # 查询结果表格
        search_result_table_layout = QHBoxLayout()
        search_result_table_layout.setContentsMargins(5, 5, 5, 5)
        search_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.search_result_table = QTableWidget()
        # self.search_result_table.setRowCount(100)  # 设置行数
        self.search_result_table.setColumnCount(3)  # 设置列数
        self.search_result_table.setHorizontalHeaderLabels(["保密员", "执行操作", "时间"])  # 设置表头
        self.search_result_table.setColumnWidth(0, 150)  # 设置列宽
        self.search_result_table.setColumnWidth(1, 400)
        self.search_result_table.setColumnWidth(2, 362)
        self.search_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        search_result_table_layout.addWidget(self.search_result_table)

        stack_shenjin_manager_w1 = QWidget()
        stack_shenjin_manager_w2 = QWidget()
        stack_shenjin_manager_w3 = QWidget()
        stack_shenjin_manager_w4 = QWidget()
        stack_shenjin_manager_w5 = QWidget()
        stack_shenjin_manager_w6 = QWidget()

        stack_shenjin_manager_w1.setLayout(search_method_layout)
        stack_shenjin_manager_w2.setLayout(search_on_time_layout)
        stack_shenjin_manager_w3.setLayout(rizhi_start_search_btn_layout)
        stack_shenjin_manager_w4.setLayout(search_result_lable_layout)
        stack_shenjin_manager_w5.setLayout(search_result_table_layout)

        stack_shenjin_manager_layout = QVBoxLayout()
        stack_shenjin_manager_layout.addWidget(stack_shenjin_manager_w1)
        stack_shenjin_manager_layout.addWidget(stack_shenjin_manager_w2)
        stack_shenjin_manager_layout.addWidget(stack_shenjin_manager_w3)
        stack_shenjin_manager_layout.addWidget(stack_shenjin_manager_w4)
        stack_shenjin_manager_layout.addWidget(stack_shenjin_manager_w5)

        self.stack_shenjin_manager.setLayout(stack_shenjin_manager_layout)

    """
    审计管理槽函数
    """
    # 按照分类查询下标返回
    def search_on_class_index(self, i):
        self.search_on_class_index_return = i

    # 日历返回时间
    def search_on_time_beg_btn_handle(self):
        self.beg_cal.show()

    def search_on_time_end_btn_handle(self):
        self.end_cal.show()

    def beg_cal_set(self):
        self.beg_data = self.beg_cal.selectedDate()
        data = self.beg_data.toString().split(" ")
        year = data[-1]
        month = data[-3][:-1]
        day = data[-2]
        self.beg_data_return = (year + "-" + month + "-" + day)

    def end_cal_set(self):
        self.end_data = self.end_cal.selectedDate()
        data = self.end_data.toString().split(" ")
        year = data[-1]
        month = data[-3][:-1]
        day = data[-2]
        self.end_data_return = (year + "-" + month + "-" + day)

    # 改变触发状态
    def shijian_choose_handle(self):
        self.search_on_time_beg_btn.setEnabled(True)
        self.search_on_time_end_btn.setEnabled(True)

    def quanbu_choose_handle(self):
        self.search_on_time_beg_btn.setEnabled(False)
        self.search_on_time_end_btn.setEnabled(False)


    # 表格增加一行数据
    def add_op_line(self, user, op, time):
        row = self.search_result_table.rowCount()
        self.search_result_table.setRowCount(row + 1)
        self.search_result_table.setItem(row, 0, QTableWidgetItem(str(user)))
        self.search_result_table.setItem(row, 1, QTableWidgetItem(str(op)))
        self.search_result_table.setItem(row, 2, QTableWidgetItem(str(time)))

    # 增加多行数据
    def add_data_to_op_table(self):
        # 清空数据表check记录
        self.search_result_table.setRowCount(0)  # 清空数据
        if self.quanbu_choose.isChecked():
            datas = get_op_record_all()
        else:
            print(self.beg_data_return, self.end_data_return)
            datas = get_op_record_time(self.beg_data_return, self.end_data_return)
        for data in datas:
            self.add_op_line(data[0], data[1], data[2])


    # 日志清除
    def stack_rizhi_delete_UI(self):
        # 选择清除时间
        delete_time_choose_layout = QHBoxLayout()
        delete_time_choose_label = QLabel("时间选择")
        delete_time_choose_label.setFont(QFont('Microsoft YaHei', 15))
        self.three_month_choose = QRadioButton("3个月前")
        self.three_month_choose.setChecked(True)  # 设置默认清除3个月之前的
        self.three_month_choose.setFont(QFont('Microsoft YaHei', 15))
        self.six_month_choose = QRadioButton("6个月前")
        self.six_month_choose.setFont(QFont('Microsoft YaHei', 15))
        self.one_year_choose = QRadioButton("1年前")
        self.one_year_choose.setFont(QFont('Microsoft YaHei', 15))
        delete_time_choose_layout.addSpacing(80)
        delete_time_choose_layout.addWidget(delete_time_choose_label)
        delete_time_choose_layout.addSpacing(100)
        delete_time_choose_layout.addWidget(self.three_month_choose)
        delete_time_choose_layout.addWidget(self.six_month_choose)
        delete_time_choose_layout.addWidget(self.one_year_choose)
        delete_time_choose_layout.addSpacing(150)

        # 开始清除按钮
        start_delete_btn_layout = QHBoxLayout()
        self.start_delete_btn = QPushButton('开始清除')
        self.start_delete_btn.clicked.connect(self.start_delete_btn_handle)
        self.start_delete_btn.setFont(QFont('Microsoft YaHei', 15))
        self.start_delete_btn.setFixedHeight(50)
        start_delete_btn_layout.addWidget(self.start_delete_btn)

        # 进度条
        delete_pbar_layout = QHBoxLayout()
        delete_pbar_label = QLabel("删除进度")
        delete_pbar_label.setFont(QFont('Microsoft YaHei', 15))
        self.delete_pbar = QProgressBar()
        self.delete_pbar.setValue(0)
        self.delete_pbar.setFixedHeight(30)
        delete_pbar_layout.addWidget(delete_pbar_label)
        delete_pbar_layout.addWidget(self.delete_pbar)

        stack_rizhi_delete_w1 = QWidget()
        stack_rizhi_delete_w2 = QWidget()
        stack_rizhi_delete_w3 = QWidget()

        stack_rizhi_delete_w1.setLayout(delete_time_choose_layout)
        stack_rizhi_delete_w2.setLayout(start_delete_btn_layout)
        stack_rizhi_delete_w3.setLayout(delete_pbar_layout)

        stack_rizhi_delete_layout = QVBoxLayout()
        stack_rizhi_delete_layout.addStretch(1)
        stack_rizhi_delete_layout.addWidget(stack_rizhi_delete_w1)
        stack_rizhi_delete_layout.addWidget(stack_rizhi_delete_w2)
        stack_rizhi_delete_layout.addWidget(stack_rizhi_delete_w3)
        stack_rizhi_delete_layout.addStretch(1)
        self.stack_rizhi_delete.setLayout(stack_rizhi_delete_layout)

    # 开始清除处理
    def start_delete_btn_handle(self):
        if self.three_month_choose.isChecked():
            remove_n_month_data(3)
            self.delete_pbar.setValue(100)
            return
        if self.six_month_choose.isChecked():
            remove_n_month_data(6)
            self.delete_pbar.setValue(100)
            return
        if self.one_year_choose.isChecked():
            remove_n_month_data(12)
            self.delete_pbar.setValue(100)
            return


    '''
    信号跳转函数
    '''
    # 信号跳转函数
    def stack_UI_display(self, i):
        self.Stack.setCurrentIndex(i)
        self.update()

    def initLayout(self):
        # 全局布局设置
        all_layout = QVBoxLayout()
        title_widget = QWidget()
        info_widget = QWidget()
        sys_guide_widget = QWidget()
        func_menu_widget = QWidget()

        title_widget.setLayout(self.title_layout)
        info_widget.setLayout(self.info_box_layout)
        sys_guide_widget.setLayout(self.sys_guide_layout)
        func_menu_widget.setLayout(self.main_menu_layout)

        all_layout.addWidget(title_widget)
        all_layout.addWidget(info_widget)
        # all_layout.addWidget(sys_guide_widget)
        all_layout.addWidget(func_menu_widget)

        self.setLayout(all_layout)

    # 初始化页面在中央显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def updateTime(self):
        self.info_box.setText(QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = Checker_Win()
    main_win.show()
    sys.exit(app.exec())

