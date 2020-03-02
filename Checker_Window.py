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
    QDesktopWidget, QStackedWidget, QComboBox, QHeaderView
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
from info_dialog import user_already_exist
from utils import database_config_save_data, save_keyword_to_keyword_lib, show_data, save_keyword_to_keyword_lib,\
    display_user_account

# 创建关键词库字典
dic_path = r"D:\实验室项目相关文档\小开发\keyword_doc\keyword_dic.docx"
d = docx.opendocx(dic_path)  # 打开数据
doc = docx.getdocumenttext(d)
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
        self.setWindowIcon(QIcon(r"./images/软件图标.ico"))
        self.resize(1200, 800)
        self.center()
        self.setFixedSize(self.width(), self.height())

        # 设置窗口样式
        win_palette = QPalette()  # 设置窗口样式
        win_palette.setBrush(QPalette.Background, QBrush(QPixmap('./images/bg3.jpg')))
        self.setPalette(win_palette)

        # 大标题
        self.title_layout = QHBoxLayout()
        title_image_label = QLabel(self)
        title_label = QLabel("数据库检查系统")
        title_label.setFont(QFont('Ink Free', 22, QFont.Bold))
        title_image_label.setPixmap(QPixmap('./images/数据库维护服务.png'))
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
        with open('QListWidgetQSS.qss', 'r') as f:
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

    """
    任务配置槽函数
    """
    # 下一步
    def stack_task_config_next_btn_handle(self):
        # self.func_menu.
        if str(self.source_add_edit.text()).strip() != "" \
                and str(self.checker_edit.text()).strip() != "" and \
                str(self.checked_edit.text()).strip() != "":
            self.Stack.setCurrentIndex(1)
        else:
            self.info_not_fill_dialog.show()

    # 保存配置
    def task_config_saved_btn_handle(self):
        check_person = str(self.checker_edit.text())
        checked_company = str(self.checked_edit.text())
        if check_person.strip() != "" and \
                checked_company.strip() != "" and \
                self.if_add_checker_checked_YES_choose.isChecked():
            database_config_save_data(check_person, checked_company)

    # 关键词配置页面
    def stack_shenjin_manager_UI(self):
        # 定义返回的查找的关键词
        self.keyword_returned_tofind = ""
        self.choose_keyword_lib_index = 0  # 初始化下标
        self.choose_which_keyword_lib_to_saved_index = 0
        # 关键词库列表
        choose_keyword_lib_comboxdata_items = []
        for keyword_content in keyword_title_dic.values():
            choose_keyword_lib_comboxdata_items.append(keyword_content)

        # 是否启用原有关键词库
        if_old_keyword_package_layout = QHBoxLayout()
        old_keyword_package_label = QLabel("是否启用原有关键词库")
        old_keyword_package_label.setFont(QFont('Microsoft YaHei', 15))
        self.old_keyword_package_YES_choose = QRadioButton("是")
        self.old_keyword_package_YES_choose.setFont(QFont('Microsoft YaHei', 15))
        self.old_keyword_package_NO_choose = QRadioButton("否")
        self.old_keyword_package_NO_choose.setChecked(True)  # 默认不用关键词库
        self.old_keyword_package_NO_choose.setFont(QFont('Microsoft YaHei', 15))
        if_old_keyword_package_layout.addSpacing(30)
        if_old_keyword_package_layout.addWidget(old_keyword_package_label)
        if_old_keyword_package_layout.addSpacing(200)
        if_old_keyword_package_layout.addWidget(self.old_keyword_package_YES_choose)
        if_old_keyword_package_layout.addWidget(self.old_keyword_package_NO_choose)
        if_old_keyword_package_layout.addSpacing(150)

        # 选择关键词库
        choose_keyword_package_layout = QHBoxLayout()
        choose_keyword_package_label = QLabel("选择关键词库")
        choose_keyword_package_label.setFont(QFont('Microsoft YaHei', 15))
        self.choose_keyword_package_combox = QComboBox()
        self.choose_keyword_package_combox.currentIndexChanged.connect(self.choose_keyword_package_index)
        self.choose_keyword_package_combox.setFixedHeight(40)
        self.choose_keyword_package_combox.setFixedWidth(500)
        self.choose_keyword_package_combox.addItems(choose_keyword_lib_comboxdata_items)
        self.keyword_package_label = QPushButton('关键词库')
        self.keyword_package_label.clicked.connect(self.click_keyword_lib_jump)  # 函数跳转
        self.keyword_package_label.setProperty('name', 'keyword_package_label')
        keyword_package_label_btn_qss = '''QPushButton[name='keyword_package_label']{background-color:rgb(255,0,0)}'''
        self.keyword_package_label.setStyleSheet(keyword_package_label_btn_qss)
        self.keyword_package_label.setFixedHeight(40)
        self.keyword_package_label.setFixedWidth(100)
        choose_keyword_package_layout.addSpacing(80)
        choose_keyword_package_layout.addWidget(choose_keyword_package_label)
        choose_keyword_package_layout.addSpacing(80)
        choose_keyword_package_layout.addWidget(self.choose_keyword_package_combox)
        choose_keyword_package_layout.addWidget(self.keyword_package_label)

        # 关键词白名单
        keyword_blank_list_layout = QHBoxLayout()
        keyword_blank_list_label = QLabel("关键词白名单")
        keyword_blank_list_label.setFont(QFont('Microsoft YaHei', 15))
        self.keyword_blank_list_edit = QLineEdit()
        self.keyword_blank_list_edit.setFixedHeight(40)
        self.keyword_blank_list_edit.setFixedWidth(500)
        keyword_blank_list_layout.addSpacing(80)
        keyword_blank_list_layout.addWidget(keyword_blank_list_label)
        keyword_blank_list_layout.addWidget(self.keyword_blank_list_edit)
        keyword_blank_list_layout.addSpacing(105)

        # 关键词搜索
        input_keyword_layout = QHBoxLayout()
        input_keyword_label = QLabel('输入关键词')
        input_keyword_label.setFont(QFont('Microsoft YaHei', 15))
        self.input_keyword_edit = QLineEdit()
        self.input_keyword_edit.setFixedHeight(40)
        self.input_keyword_edit.setFixedWidth(500)
        input_keyword_layout.addSpacing(80)
        input_keyword_layout.addWidget(input_keyword_label)
        input_keyword_layout.addWidget(self.input_keyword_edit)
        input_keyword_layout.addSpacing(105)

        # 是否将关键词添加到词库
        if_add_to_keyword_package_layout = QHBoxLayout()
        if_add_to_keyword_package_label = QLabel("关键词是否添加到词库")
        if_add_to_keyword_package_label.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_to_keyword_package_YES_choose = QRadioButton("是")
        self.if_add_to_keyword_package_YES_choose.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_to_keyword_package_NO_choose = QRadioButton("否")
        self.if_add_to_keyword_package_NO_choose.setChecked(True)  # 默认不用关键词库
        self.if_add_to_keyword_package_NO_choose.setFont(QFont('Microsoft YaHei', 15))
        if_add_to_keyword_package_layout.addSpacing(30)
        if_add_to_keyword_package_layout.addWidget(if_add_to_keyword_package_label)
        if_add_to_keyword_package_layout.addSpacing(200)
        if_add_to_keyword_package_layout.addWidget(self.if_add_to_keyword_package_YES_choose)
        if_add_to_keyword_package_layout.addWidget(self.if_add_to_keyword_package_NO_choose)
        if_add_to_keyword_package_layout.addSpacing(150)

        # 选择要保存的关键词库
        choose_which_keyword_package_to_saved_layout = QHBoxLayout()
        choose_which_keyword_package_to_saved_label = QLabel('选择要保存的关键词库')
        choose_which_keyword_package_to_saved_label.setFont(QFont('Microsoft YaHei', 15))
        self.choose_which_keyword_package_to_saved_combox = QComboBox()
        self.choose_which_keyword_package_to_saved_combox.currentIndexChanged.connect(self.choose_which_keyword_package_to_saved_index)
        self.choose_which_keyword_package_to_saved_combox.addItems(choose_keyword_lib_comboxdata_items)

        self.choose_which_keyword_package_to_saved_combox.setFixedHeight(40)
        self.choose_which_keyword_package_to_saved_combox.setFixedWidth(500)
        choose_which_keyword_package_to_saved_layout.addSpacing(30)
        choose_which_keyword_package_to_saved_layout.addWidget(choose_which_keyword_package_to_saved_label)
        choose_which_keyword_package_to_saved_layout.addSpacing(50)
        choose_which_keyword_package_to_saved_layout.addWidget(self.choose_which_keyword_package_to_saved_combox)
        choose_which_keyword_package_to_saved_layout.addSpacing(150)

        # 保存配置按钮
        stack_keyword_saved_layout = QHBoxLayout()
        self.stack_keyword_save_btn = QPushButton('保存配置')
        self.stack_keyword_save_btn.clicked.connect(self.keyword_save_btn_handle)
        self.stack_keyword_save_btn.setFont(QFont('Microsoft YaHei', 15))
        self.stack_keyword_save_btn.setProperty('name', 'stack_keyword_save_btn')  # 设置按钮属性
        stack_keyword_save_btn_qss = '''QPushButton[name='stack_keyword_save_btn']{background-color:rgb(0,255,255)}'''
        self.stack_keyword_save_btn.setStyleSheet(stack_keyword_save_btn_qss)
        self.stack_keyword_save_btn.setFixedHeight(60)
        stack_keyword_saved_layout.addWidget(self.stack_keyword_save_btn)

        # 下一步
        stack_keyword_next_layout = QHBoxLayout()
        self.stack_keyword_next_btn = QPushButton("下一步")
        self.stack_keyword_next_btn.clicked.connect(self.stack_keyword_next_btn_handle)
        self.stack_keyword_next_btn.setFont(QFont('Microsoft YaHei', 15))
        self.stack_keyword_next_btn.setFixedHeight(60)
        stack_keyword_next_layout.addWidget(self.stack_keyword_next_btn)

        stack_keyword_w1 = QWidget()
        stack_keyword_w2 = QWidget()
        stack_keyword_w3 = QWidget()
        stack_keyword_w4 = QWidget()
        stack_keyword_w5 = QWidget()
        stack_keyword_w6 = QWidget()
        stack_keyword_w7 = QWidget()
        stack_keyword_w8 = QWidget()

        stack_keyword_w1.setLayout(if_old_keyword_package_layout)
        stack_keyword_w2.setLayout(choose_keyword_package_layout)
        stack_keyword_w3.setLayout(keyword_blank_list_layout)
        stack_keyword_w4.setLayout(input_keyword_layout)
        stack_keyword_w5.setLayout(if_add_to_keyword_package_layout)
        stack_keyword_w6.setLayout(choose_which_keyword_package_to_saved_layout)
        stack_keyword_w7.setLayout(stack_keyword_saved_layout)
        stack_keyword_w8.setLayout(stack_keyword_next_layout)

        stack_keyword_layout = QVBoxLayout()
        stack_keyword_layout.addWidget(stack_keyword_w1)
        stack_keyword_layout.addWidget(stack_keyword_w2)
        stack_keyword_layout.addWidget(stack_keyword_w3)
        stack_keyword_layout.addWidget(stack_keyword_w4)
        stack_keyword_layout.addWidget(stack_keyword_w5)
        stack_keyword_layout.addWidget(stack_keyword_w6)
        stack_keyword_layout.addWidget(stack_keyword_w7)
        stack_keyword_layout.addWidget(stack_keyword_w8)

        self.stack_shenjin_manager.setLayout(stack_keyword_layout)

    """
    关键词配置槽函数
    """
    # 下一步按钮
    def stack_keyword_next_btn_handle(self):
        self.Stack.setCurrentIndex(2)

    # 关键词库跳转
    def click_keyword_lib_jump(self):
        self.keyword_dialog.show()

    # 选择关键词库
    def choose_keyword_package_index(self, i):
        self.choose_keyword_lib_index = (i + 1)

    def choose_which_keyword_package_to_saved_index(self, i):
        self.choose_which_keyword_lib_to_saved_index = (i + 1)

    # 保存配置
    def keyword_save_btn_handle(self):
        if self.old_keyword_package_NO_choose.isChecked():  # 不启用关键词库
            self.keyword_returned_tofind = ""
            self.keyword_returned_tofind = str(self.input_keyword_edit.text())
        else:
            self.keyword_returned_tofind = ""
            data = show_data("keyword" + str(self.choose_keyword_lib_index))
            for keyword_pair in data:
                self.keyword_returned_tofind += (keyword_pair[1] + " ")
            print(self.keyword_returned_tofind)
        if self.if_add_to_keyword_package_YES_choose.isChecked():  # 保存到关键词库
            keyword = "keyword" + str(self.choose_which_keyword_lib_to_saved_index)
            save_keyword_to_keyword_lib(str(self.input_keyword_edit.text()), keyword)

    # 数据库发现页面
    def stack_rizhi_delete_UI(self):
        # 开始探测数据库服务器
        start_find_db_add_layout = QHBoxLayout()
        start_find_db_add_layout.setContentsMargins(5, 5, 5, 5)
        self.start_find_db_add_btn = QPushButton("开始探测数据库服务器")
        self.start_find_db_add_btn.setFixedHeight(60)
        self.start_find_db_add_btn.setFixedWidth(1000)
        self.start_find_db_add_btn.setFont(QFont('Microsoft YaHei', 15))
        start_find_db_add_layout.addWidget(self.start_find_db_add_btn)

        # 探测结果标题
        search_result_title_layout = QHBoxLayout()
        search_result_title_layout.setContentsMargins(5, 5, 5, 5)
        search_result_title = QLabel("探测结果")
        search_result_title.setFont(QFont('Microsoft YaHei', 10))
        search_result_title_layout.addStretch(1)
        search_result_title_layout.addWidget(search_result_title)
        search_result_title_layout.addStretch(1)

        # 探测结果表格
        search_result_table_layout = QHBoxLayout()
        search_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.search_result_table = QTableWidget()
        self.search_result_table.setRowCount(100)  # 设置行数
        self.search_result_table.setColumnCount(3)  # 设置列数
        self.search_result_table.setHorizontalHeaderLabels(["IP端口", "数据库类型", "是否加入检查"])  # 设置表头
        self.search_result_table.setColumnWidth(0, 100)  # 设置列宽
        self.search_result_table.setColumnWidth(1, 400)
        self.search_result_table.setColumnWidth(2, 400)
        self.search_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        search_result_table_layout.addWidget(self.search_result_table)

        # 检查进度
        search_schedule_display_layout = QHBoxLayout()
        search_schedule_display_layout.setContentsMargins(5, 5, 5, 5)
        search_schedule_display_label = QLabel("检查进度")
        search_schedule_display_label.setFont(QFont('Microsoft YaHei', 15))
        self.search_schedule_pbar = QProgressBar()
        self.search_schedule_pbar.setValue(50)
        self.search_schedule_pbar.setFixedHeight(30)
        search_schedule_display_layout.addWidget(search_schedule_display_label)
        search_schedule_display_layout.addWidget(self.search_schedule_pbar)

        # 终止检查按钮
        db_end_search_btn_layout = QHBoxLayout()
        db_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.db_end_search_btn = QPushButton("终止检查")
        self.db_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.db_end_search_btn.setProperty('name', 'db_end_search_btn')
        db_end_search_btn_qss = '''QPushButton[name='db_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.db_end_search_btn.setStyleSheet(db_end_search_btn_qss)
        self.db_end_search_btn.setFixedHeight(40)
        db_end_search_btn_layout.addWidget(self.db_end_search_btn)

        # 选择完成，开始检查按钮
        db_choose_finished_layout = QHBoxLayout()
        db_choose_finished_layout.setContentsMargins(5, 5, 5, 5)
        self.db_choose_finished_btn = QPushButton("选择完成，开始进行检查")
        # self.db_choose_finished_btn.clicked.connect(self.stack_db_search_db_choose_finished_btn_handle)
        self.db_choose_finished_btn.setFont(QFont('Microsoft YaHei', 15))
        self.db_choose_finished_btn.setFixedHeight(40)
        db_choose_finished_layout.addWidget(self.db_choose_finished_btn)

        stack_db_search_w1 = QWidget()
        stack_db_search_w2 = QWidget()
        stack_db_search_w3 = QWidget()
        stack_db_search_w4 = QWidget()
        stack_db_search_w5 = QWidget()
        stack_db_search_w6 = QWidget()

        stack_db_search_w1.setLayout(start_find_db_add_layout)
        stack_db_search_w2.setLayout(search_result_title_layout)
        stack_db_search_w3.setLayout(search_result_table_layout)
        stack_db_search_w4.setLayout(search_schedule_display_layout)
        stack_db_search_w5.setLayout(db_end_search_btn_layout)
        stack_db_search_w6.setLayout(db_choose_finished_layout)

        stack_db_search_layout = QVBoxLayout()
        stack_db_search_layout.setSpacing(0)
        stack_db_search_layout.addWidget(stack_db_search_w1)
        stack_db_search_layout.addWidget(stack_db_search_w2)
        stack_db_search_layout.addWidget(stack_db_search_w3)
        # stack_db_search_layout.addStretch(5)
        stack_db_search_layout.addWidget(stack_db_search_w4)
        stack_db_search_layout.addWidget(stack_db_search_w5)
        stack_db_search_layout.addWidget(stack_db_search_w6)
        self.stack_rizhi_delete.setLayout(stack_db_search_layout)

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

