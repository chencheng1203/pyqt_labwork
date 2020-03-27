# -*- encoding:utf-8 -*-
# @Time: 2020/1/1 15:02

import sys
sys.path.append(r"D:\Code\PyQt\bupt_prj01\keyword_search")
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QCheckBox, \
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QProgressBar,\
    QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QAbstractItemView, \
    QDesktopWidget, QStackedWidget, QComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
from utils import get_current_time
import PyQt5.QtCore as QtCore
from keyword_Lib_dialog import KeywordLib_Dialog
from utils import database_config_save_data, save_keyword_to_keyword_lib, show_data, save_keyword_to_keyword_lib, \
    insert_op_record, read_data_from_keyword_dic_table, file_check_record_insert, file_check_conf_return
from keyword_search.wb import get_file_keyword_all
from info_dialog import info_not_fill

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

class MainWin(QWidget):
    def __init__(self):
        super(MainWin, self).__init__()

        # 右侧控件设置
        self.stack_task_config = QWidget()  # 任务配置控件
        self.stack_keyword = QWidget()  # 关键词
        self.stack_db_search = QWidget()  # 数据库发现
        self.stack_file_check = QWidget()  # 文件检查
        self.stack_email_check = QWidget()  # 邮件检查
        self.stack_pic_check = QWidget()  # 图片检查
        self.stack_db_log_check = QWidget()  # 数据库日志检查
        self.stack_security_scan = QWidget()  # 数据库安全扫描
        self.stack_second_check = QWidget()  # 二次检索
        self.stack_result = QWidget()  # 检查结果

        # 跳转窗口初始化
        self.keyword_dialog = KeywordLib_Dialog()
        # 完善信息提示
        self.info_not_fill_dialog = info_not_fill()
        # 设置当前用户
        self.current_user = ""
        # 文件检查标记等级设置
        self.file_check_degree_select_combox = []
        # 标识本次检索的id号
        self.check_id = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss dddd')[:-4].\
            replace('-', '').replace(':', '').replace(' ', '')
        # 文件检查的对应的数据存储
        self.file_check_fileName_saved = []
        self.file_check_keyword_saved = []

        print(self.check_id)

        self.initUI()  # 基本信息初始化
        self.initLayout()  # 布局初始化

    def set_current_user(self, user):
        self.current_user = user

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
        title_image_label.setPixmap(QPixmap(r'D:\Code\PyQt\bupt_prj01\images/数据库维护服务.png'))
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
        list_items = ['任务配置', '关键词配置', '数据库发现', '文件检查', '邮件检查',\
                      '图片检查', '数据库日志检查', '数据库安全扫描', '二次检索', '检查结果']
        for i in range(len(list_items)):
            self.item = QListWidgetItem(list_items[i], self.func_menu)
            self.item.setSizeHint(QSize(25, 62))
            self.item.setTextAlignment(Qt.AlignCenter)
            # func_menu.insertItem(i, list_items[i])
        self.func_menu.currentRowChanged.connect(self.stack_UI_display)  # 连接信号

        # 右侧控件设置
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack_task_config)
        self.Stack.addWidget(self.stack_keyword)
        self.Stack.addWidget(self.stack_db_search)
        self.Stack.addWidget(self.stack_file_check)
        self.Stack.addWidget(self.stack_email_check)
        self.Stack.addWidget(self.stack_pic_check)
        self.Stack.addWidget(self.stack_db_log_check)
        self.Stack.addWidget(self.stack_security_scan)
        self.Stack.addWidget(self.stack_second_check)
        self.Stack.addWidget(self.stack_result)

        self.main_menu_layout = QHBoxLayout()
        self.main_menu_layout.addWidget(self.func_menu)
        self.main_menu_layout.addWidget(self.Stack)

        self.stack_task_config_UI()
        self.stack_keyword_UI()
        self.stack_db_search_UI()
        self.stack_file_check_UI()
        self.stack_email_check_UI()
        self.stack_pic_check_UI()
        self.stack_db_log_check_UI()
        self.stack_security_scan_UI()
        self.stack_second_check_UI()
        self.stack_result_UI()

        # self.mian_menu_layout.addSpacing(1000)

    # 任务配置页面
    def stack_task_config_UI(self):
        # 数据源地址
        source_add_layout = QHBoxLayout()
        source_add_label = QLabel("数据源地址")
        source_add_label.setFont(QFont('Microsoft YaHei', 15))
        self.source_add_edit = QLineEdit()
        self.source_add_edit.setFixedWidth(600)
        self.source_add_edit.setFixedHeight(40)
        source_add_layout.addSpacing(70)
        source_add_layout.addWidget(source_add_label)
        source_add_layout.addSpacing(70)
        source_add_layout.addWidget(self.source_add_edit)
        source_add_layout.addSpacing(300)

        # 文件过滤控件
        # if_open_file_filter_layout = QHBoxLayout()
        # if_open_file_filter_label = QLabel("是否启用文件过滤")
        # if_open_file_filter_label.setFont(QFont('Microsoft YaHei', 15))
        # self.if_open_file_filter_YES_choose = QRadioButton("是")
        # self.if_open_file_filter_YES_choose.setFont(QFont('Microsoft YaHei', 15))
        # self.if_open_file_filter_NO_choose = QRadioButton("否")
        # self.if_open_file_filter_NO_choose.setChecked(True)  # 默认选中
        # self.if_open_file_filter_NO_choose.setFont(QFont('Microsoft YaHei', 15))
        # if_open_file_filter_layout.addSpacing(30)  # 布局信息
        # if_open_file_filter_layout.addWidget(if_open_file_filter_label)
        # if_open_file_filter_layout.addSpacing(150)
        # if_open_file_filter_layout.addWidget(self.if_open_file_filter_YES_choose)
        # if_open_file_filter_layout.addWidget(self.if_open_file_filter_NO_choose)
        # if_open_file_filter_layout.addSpacing(160)

        # 是否添加审查人和被审查单位
        if_add_checker_checked_layout = QHBoxLayout()
        if_add_checker_checked_label = QLabel("是否添加审查信息")
        if_add_checker_checked_label.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_checker_checked_YES_choose = QRadioButton("是")
        self.if_add_checker_checked_YES_choose.setChecked(True)  # 默认选中
        self.if_add_checker_checked_YES_choose.setFont(QFont('Microsoft YaHei', 15))
        self.if_add_checker_checked_NO_choose = QRadioButton("否")
        self.if_add_checker_checked_NO_choose.setFont(QFont('Microsoft YaHei', 15))
        # 布局信息
        if_add_checker_checked_layout.addSpacing(30)
        if_add_checker_checked_layout.addWidget(if_add_checker_checked_label)
        if_add_checker_checked_layout.addSpacing(150)
        if_add_checker_checked_layout.addWidget(self.if_add_checker_checked_YES_choose)
        if_add_checker_checked_layout.addWidget(self.if_add_checker_checked_NO_choose)
        if_add_checker_checked_layout.addSpacing(160)

        # 审查人
        checker_layout = QHBoxLayout()
        checker_label = QLabel("审查人")
        checker_label.setFont(QFont('Microsoft YaHei', 15))
        self.checker_edit = QLineEdit()
        self.checker_edit.setFixedWidth(600)
        self.checker_edit.setFixedHeight(40)
        checker_layout.addSpacing(90)
        checker_layout.addWidget(checker_label)
        checker_layout.addSpacing(100)
        checker_layout.addWidget(self.checker_edit)
        checker_layout.addSpacing(160)

        # 被审查单位
        checked_layout = QHBoxLayout()
        checked_label = QLabel("被审查单位")
        checked_label.setFont(QFont('Microsoft YaHei', 15))
        self.checked_edit = QLineEdit()
        self.checked_edit.setFixedWidth(600)
        self.checked_edit.setFixedHeight(40)
        checked_layout.addSpacing(70)
        checked_layout.addWidget(checked_label)
        checked_layout.addSpacing(70)
        checked_layout.addWidget(self.checked_edit)
        checked_layout.addSpacing(160)

        # 保存配置按钮
        stack_task_config_saved_layout = QHBoxLayout()
        self.stack_task_config_saved_btn = QPushButton("保存配置")
        self.stack_task_config_saved_btn.clicked.connect(self.task_config_saved_btn_handle)  # 槽函数
        self.stack_task_config_saved_btn.setFixedHeight(60)
        self.stack_task_config_saved_btn.setProperty('name', 'stack_task_config_saved_btn')  # 设置按钮属性
        stack_task_config_saved_btn_qss = '''QPushButton[name='stack_task_config_saved_btn']{background-color:rgb(0,255,255)}'''
        self.stack_task_config_saved_btn.setFont(QFont('Microsoft YaHei', 15))
        self.stack_task_config_saved_btn.setStyleSheet(stack_task_config_saved_btn_qss)
        stack_task_config_saved_layout.addWidget(self.stack_task_config_saved_btn)

        # 下一步按钮
        stack_task_config_next_layout = QHBoxLayout()
        self.stack_task_config_next_btn = QPushButton("下一步")
        self.stack_task_config_next_btn.clicked.connect(self.stack_task_config_next_btn_handle)
        self.stack_task_config_next_btn.setFixedHeight(60)
        self.stack_task_config_next_btn.setFont(QFont('Microsoft YaHei', 15))
        stack_task_config_next_layout.addWidget(self.stack_task_config_next_btn)

        stack_task_config_w1 = QWidget()
        stack_task_config_w2 = QWidget()
        stack_task_config_w3 = QWidget()
        stack_task_config_w4 = QWidget()
        stack_task_config_w5 = QWidget()
        stack_task_config_w6 = QWidget()
        stack_task_config_w7 = QWidget()

        stack_task_config_w1.setLayout(source_add_layout)
        # stack_task_config_w2.setLayout(if_open_file_filter_layout)
        stack_task_config_w3.setLayout(if_add_checker_checked_layout)
        stack_task_config_w4.setLayout(checker_layout)
        stack_task_config_w5.setLayout(checked_layout)
        stack_task_config_w6.setLayout(stack_task_config_saved_layout)
        stack_task_config_w7.setLayout(stack_task_config_next_layout)

        stack_task_config_layout = QVBoxLayout()
        stack_task_config_layout.addWidget(stack_task_config_w1)
        # stack_task_config_layout.addWidget(stack_task_config_w2)
        stack_task_config_layout.addWidget(stack_task_config_w3)
        stack_task_config_layout.addWidget(stack_task_config_w4)
        stack_task_config_layout.addWidget(stack_task_config_w5)
        stack_task_config_layout.addWidget(stack_task_config_w6)
        stack_task_config_layout.addWidget(stack_task_config_w7)

        self.stack_task_config.setLayout(stack_task_config_layout)

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
        else:
            insert_op_record(self.current_user, "任务配置")

    # 关键词配置页面
    def stack_keyword_UI(self):
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

        self.stack_keyword.setLayout(stack_keyword_layout)

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
            self.keyword_returned_tofind = str(self.input_keyword_edit.text())
            insert_op_record(self.current_user, "关键词配置-不启用关键词库")
        else:
            self.keyword_returned_tofind = ""
            data = show_data("keyword" + str(self.choose_keyword_lib_index))
            for keyword_pair in data:
                self.keyword_returned_tofind += (keyword_pair[1] + " ")
            insert_op_record(self.current_user, "选择关键词库-" + keyword_title_dic["keyword" + str(self.choose_keyword_lib_index)])
        print(self.keyword_returned_tofind)
        if self.if_add_to_keyword_package_YES_choose.isChecked():  # 保存到关键词库
            keyword = "keyword" + str(self.choose_which_keyword_lib_to_saved_index)
            save_keyword_to_keyword_lib(str(self.input_keyword_edit.text()), keyword)
            insert_op_record(self.current_user, "添加关键词")

    # 数据库发现页面
    def stack_db_search_UI(self):
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
        self.db_choose_finished_btn.clicked.connect(self.stack_db_search_db_choose_finished_btn_handle)
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
        self.stack_db_search.setLayout(stack_db_search_layout)

    """
    数据库发现槽函数
    """
    def stack_db_search_db_choose_finished_btn_handle(self):
        insert_op_record(self.current_user, "数据库发现")
        self.Stack.setCurrentIndex(3)


    # 文件检查页面
    def stack_file_check_UI(self):
        # 选择检查的数据类型
        choose_file_type_to_check_layout = QHBoxLayout()
        choose_file_type_to_check_layout.setContentsMargins(5, 5, 5, 5)
        choose_file_type_to_check_label = QLabel("选择检查的数据类型")
        choose_file_type_to_check_label.setFont(QFont('Microsoft YaHei', 15))
        self.choose_file_type_to_check_word = QCheckBox("word")
        self.choose_file_type_to_check_word.setFont(QFont('Microsoft YaHei', 15))
        self.choose_file_type_to_check_pdf = QCheckBox("pdf")
        self.choose_file_type_to_check_pdf.setFont(QFont('Microsoft YaHei', 15))
        self.choose_file_type_to_check_txt = QCheckBox("txt")
        self.choose_file_type_to_check_txt.setFont(QFont('Microsoft YaHei', 15))
        choose_file_type_to_check_layout.addWidget(choose_file_type_to_check_label)
        choose_file_type_to_check_layout.addSpacing(100)
        choose_file_type_to_check_layout.addWidget(self.choose_file_type_to_check_word)
        choose_file_type_to_check_layout.addWidget(self.choose_file_type_to_check_pdf)
        choose_file_type_to_check_layout.addWidget(self.choose_file_type_to_check_txt)

        # 文件检查-开始检查
        file_check_start_check_layout = QHBoxLayout()
        file_check_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.file_check_start_check_btn = QPushButton("开始检查")
        self.file_check_start_check_btn.clicked.connect(self.file_check_start_check_btn_handle)
        self.file_check_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.file_check_start_check_btn.setFixedHeight(60)
        file_check_start_check_layout.addWidget(self.file_check_start_check_btn)

        # 文件检查-检查结果标签
        file_check_check_result_layout = QHBoxLayout()
        file_check_check_result_layout.setContentsMargins(5, 5, 5, 5)
        file_check_check_result_label = QLabel("检查结果")
        file_check_check_result_label.setFont(QFont('Microsoft YaHei', 10))
        file_check_check_result_layout.addStretch(1)
        file_check_check_result_layout.addWidget(file_check_check_result_label)
        file_check_check_result_layout.addStretch(1)

        # 文件检查-检查结果表格
        file_check_check_result_table_layout = QHBoxLayout()
        file_check_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.file_check_check_result_table = QTableWidget()
        # self.file_check_check_result_table.setRowCount(100)  # 设置行数
        self.file_check_check_result_table.setColumnCount(5)  # 设置列数
        self.file_check_check_result_table.setHorizontalHeaderLabels(["IP端口", "文件名", "检查出的关键字", "置信度等级", "选择涉密等级"])  # 设置表头
        self.file_check_check_result_table.setColumnWidth(0, 100)  # 设置列宽
        self.file_check_check_result_table.setColumnWidth(1, 260)
        self.file_check_check_result_table.setColumnWidth(2, 200)
        self.file_check_check_result_table.setColumnWidth(3, 100)
        self.file_check_check_result_table.setColumnWidth(4, 200)
        self.file_check_check_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        file_check_check_result_table_layout.addWidget(self.file_check_check_result_table)

        # 检查进度
        file_check_check_pbar_layout = QHBoxLayout()
        file_check_check_pbar_layout.setContentsMargins(5, 5, 5, 5)
        file_check_check_display_label = QLabel("检查进度")
        file_check_check_display_label.setFont(QFont('Microsoft YaHei', 15))
        self.file_check_check_pbar = QProgressBar()
        self.file_check_check_pbar.setValue(0)
        self.file_check_check_pbar.setFixedHeight(30)
        file_check_check_pbar_layout.addWidget(file_check_check_display_label)
        file_check_check_pbar_layout.addWidget(self.file_check_check_pbar)

        # 终止检查按钮
        file_check_end_search_btn_layout = QHBoxLayout()
        file_check_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.file_check_end_search_btn = QPushButton("终止检查")
        self.file_check_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.file_check_end_search_btn.setProperty('name', 'file_check_end_search_btn')
        db_end_search_btn_qss = '''QPushButton[name='file_check_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.file_check_end_search_btn.setStyleSheet(db_end_search_btn_qss)
        self.file_check_end_search_btn.setFixedHeight(40)
        file_check_end_search_btn_layout.addWidget(self.file_check_end_search_btn)

        # 选择完成，开始检查按钮
        file_check_finished_layout = QHBoxLayout()
        file_check_finished_layout.setContentsMargins(5, 5, 5, 5)
        self.file_check_finished_btn = QPushButton("保存标记结果")
        self.file_check_finished_btn.clicked.connect(self.file_check_finished_btn_handle)
        self.file_check_finished_btn.setFont(QFont('Microsoft YaHei', 15))
        self.file_check_finished_btn.setFixedHeight(40)

        # 二次检索按钮
        self.file_check_second_search_btn = QPushButton("二次检索")
        self.file_check_second_search_btn.setProperty('name', 'file_check_second_search_btn')
        self.file_check_second_search_btn.setFixedHeight(40)
        self.file_check_second_search_btn.setFixedWidth(100)
        file_check_second_search_btn_qss = '''QPushButton[name='file_check_second_search_btn']{background-color:rgb(0,255,255)}'''
        self.file_check_second_search_btn.setStyleSheet(file_check_second_search_btn_qss)
        file_check_finished_layout.addWidget(self.file_check_finished_btn)
        file_check_finished_layout.addWidget(self.file_check_second_search_btn)

        stack_file_check_w1 = QWidget()
        stack_file_check_w2 = QWidget()
        stack_file_check_w3 = QWidget()
        stack_file_check_w4 = QWidget()
        stack_file_check_w5 = QWidget()
        stack_file_check_w6 = QWidget()
        stack_file_check_w7 = QWidget()
        stack_file_check_w8 = QWidget()

        stack_file_check_w1.setLayout(choose_file_type_to_check_layout)
        stack_file_check_w2.setLayout(file_check_start_check_layout)
        stack_file_check_w3.setLayout(file_check_check_result_layout)
        stack_file_check_w4.setLayout(file_check_check_result_table_layout)
        stack_file_check_w5.setLayout(file_check_check_pbar_layout)
        stack_file_check_w6.setLayout(file_check_end_search_btn_layout)
        stack_file_check_w7.setLayout(file_check_finished_layout)
        # stack_file_check_w8.setLayout(file_check_second_search_layout)

        stack_file_check_layout = QVBoxLayout()
        stack_file_check_layout.setSpacing(0)
        stack_file_check_layout.addWidget(stack_file_check_w1)
        stack_file_check_layout.addWidget(stack_file_check_w2)
        stack_file_check_layout.addWidget(stack_file_check_w3)
        stack_file_check_layout.addWidget(stack_file_check_w4)
        stack_file_check_layout.addWidget(stack_file_check_w5)
        stack_file_check_layout.addWidget(stack_file_check_w6)
        stack_file_check_layout.addWidget(stack_file_check_w7)
        # stack_file_check_layout.addWidget(stack_file_check_w8)

        self.stack_file_check.setLayout(stack_file_check_layout)

    # 向文件检查表格中插入数据
    # 表格增加一行数据
    def file_check_add_line(self, ip="127.0.0.1", file_name="", keyword="", conf_class="3", sect_class="2"):
        row = self.file_check_check_result_table.rowCount()

        combox = QComboBox()
        combox.setFixedHeight(20)
        # combox.setFixedWidth(50)
        combox.addItems(["可疑", "秘密", "机密", "绝密"])
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(combox)
        w = QWidget()
        w.setLayout(h)

        self.file_check_check_result_table.setRowCount(row + 1)
        self.file_check_check_result_table.setItem(row, 0, QTableWidgetItem(ip))
        self.file_check_check_result_table.setItem(row, 1, QTableWidgetItem(file_name))
        self.file_check_check_result_table.setItem(row, 2, QTableWidgetItem(keyword))
        self.file_check_check_result_table.setItem(row, 3, QTableWidgetItem(conf_class))
        self.file_check_check_result_table.setCellWidget(row, 4, w)
        self.file_check_degree_select_combox.append(combox)
        # self.file_check_check_result_table.setItem(row, 4, QTableWidgetItem(sect_class))

    # 增加多行数据
    def file_check_add_data_to_table(self):
        self.file_check_check_result_table.setRowCount(0)  # 清空数据
        datas = get_file_keyword_all(keyword=self.keyword_returned_tofind, number=4)
        keyword_datas = datas[0]
        # print(keyword_datas)
        # 保存文件名和关键字，清空数据
        self.file_check_fileName_saved = []
        self.file_check_keyword_saved = []
        count_datas = datas[1]
        count = 0
        conf_data = str(file_check_conf_return(self.keyword_returned_tofind))
        for key_data in keyword_datas.keys():
            for values in keyword_datas[key_data]:
                count += 1
                self.file_check_check_pbar.setValue((count / count_datas * 100))
                self.file_check_add_line(file_name=str(key_data), conf_class=conf_data, keyword=str(values))
                self.file_check_fileName_saved.append(str(key_data))
                self.file_check_keyword_saved.append(str(values))

    # 处理函数
    def file_check_start_check_btn_handle(self):
        self.file_check_check_pbar.setValue(10)
        insert_op_record(self.current_user, "文件检查")
        self.file_check_add_data_to_table()

    # 保存标记结果
    def file_check_finished_btn_handle(self):
        for i, check_id in enumerate(self.file_check_degree_select_combox):
            degree_selected = check_id.currentIndex()
            file_check_fileName = self.file_check_fileName_saved[i]
            file_check_keyword = self.file_check_keyword_saved[i]
            # print(degree_selected, file_check_fileName, file_check_keyword)
            file_check_record_insert(self.check_id, "127.0.0.1", file_check_fileName, self.keyword_returned_tofind, file_check_keyword, str(degree_selected))


    # 邮件检查页面
    def stack_email_check_UI(self):
        # 用户名及密码
        email_check_login_layout = QHBoxLayout()
        email_check_login_layout.setContentsMargins(5, 5, 5, 5)
        email_check_user_label = QLabel("邮箱用户名")
        email_check_user_label.setFont(QFont('Microsoft YaHei', 12))
        self.email_check_user_edit = QLineEdit()
        self.email_check_user_edit.setFixedHeight(30)
        email_check_passwd_label = QLabel("邮箱密码")
        email_check_passwd_label.setFont(QFont('Microsoft YaHei', 12))
        self.email_check_passwd_edit = QLineEdit()
        self.email_check_passwd_edit.setFixedHeight(30)
        email_check_login_layout.addWidget(email_check_user_label)
        email_check_login_layout.addSpacing(30)
        email_check_login_layout.addWidget(self.email_check_user_edit)
        email_check_login_layout.addSpacing(50)
        email_check_login_layout.addWidget(email_check_passwd_label)
        email_check_login_layout.addSpacing(30)
        email_check_login_layout.addWidget(self.email_check_passwd_edit)
        email_check_login_layout.addSpacing(7)

        # 邮件协议类型
        email_check_protocol_type_layout = QHBoxLayout()
        email_check_protocol_type_layout.setContentsMargins(5, 5, 5, 5)
        email_check_protocol_type_label = QLabel("邮件协议类型")
        email_check_protocol_type_label.setFont(QFont('Microsoft YaHei', 12))
        self.email_check_protocol_type_combox = QComboBox()
        self.email_check_protocol_type_combox.setFixedHeight(30)
        self.email_check_protocol_type_combox.setFixedWidth(820)
        self.email_check_protocol_type_combox.addItems(["IMAP", "POP3"])
        email_check_protocol_type_layout.addWidget(email_check_protocol_type_label)
        # email_check_protocol_type_layout.addSpacing(7)
        email_check_protocol_type_layout.addWidget(self.email_check_protocol_type_combox)
        email_check_protocol_type_layout.addSpacing(7)

        # 邮件检查-开始检查
        email_check_start_check_layout = QHBoxLayout()
        email_check_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.email_check_start_check_btn = QPushButton("开始检查")
        self.email_check_start_check_btn.clicked.connect(self.email_check_start_check_btn_handle)
        self.email_check_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.email_check_start_check_btn.setFixedHeight(60)
        email_check_start_check_layout.addWidget(self.email_check_start_check_btn)

        # 邮件检查-检查结果标签
        email_check_check_result_layout = QHBoxLayout()
        email_check_check_result_layout.setContentsMargins(5, 5, 5, 5)
        email_check_check_result_label = QLabel("检查结果")
        email_check_check_result_label.setFont(QFont('Microsoft YaHei', 10))
        email_check_check_result_layout.addStretch(1)
        email_check_check_result_layout.addWidget(email_check_check_result_label)
        email_check_check_result_layout.addStretch(1)

        # 邮件检查-检查结果表格
        email_check_check_result_table_layout = QHBoxLayout()
        email_check_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.email_check_check_result_table = QTableWidget()
        self.email_check_check_result_table.setRowCount(100)  # 设置行数
        self.email_check_check_result_table.setColumnCount(5)  # 设置列数
        self.email_check_check_result_table.setHorizontalHeaderLabels(["邮箱", "标题", "检查出的关键字", "置信度等级", "选择涉密等级"])  # 设置表头
        self.email_check_check_result_table.setColumnWidth(0, 100)  # 设置列宽
        self.email_check_check_result_table.setColumnWidth(1, 200)
        self.email_check_check_result_table.setColumnWidth(2, 200)
        self.email_check_check_result_table.setColumnWidth(3, 200)
        self.email_check_check_result_table.setColumnWidth(4, 180)
        self.email_check_check_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        email_check_check_result_table_layout.addWidget(self.email_check_check_result_table)

        # 检查进度
        email_check_check_pbar_layout = QHBoxLayout()
        email_check_check_pbar_layout.setContentsMargins(5, 5, 5, 5)
        email_check_check_pbar_label = QLabel("检查进度")
        email_check_check_pbar_label.setFont(QFont('Microsoft YaHei', 10))
        self.email_check_check_pbar = QProgressBar()
        self.email_check_check_pbar.setValue(50)
        self.email_check_check_pbar.setFixedHeight(40)
        email_check_check_pbar_layout.addWidget(email_check_check_pbar_label)
        email_check_check_pbar_layout.addWidget(self.email_check_check_pbar)

        # 终止检查按钮
        email_check_end_search_btn_layout = QHBoxLayout()
        email_check_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.email_check_end_search_btn = QPushButton("终止检查")
        self.email_check_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.email_check_end_search_btn.setProperty('name', 'email_check_end_search_btn')
        email_end_search_btn_qss = '''QPushButton[name='email_check_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.email_check_end_search_btn.setStyleSheet(email_end_search_btn_qss)
        self.email_check_end_search_btn.setFixedHeight(40)
        email_check_end_search_btn_layout.addWidget(self.email_check_end_search_btn)

        # 选择完成，开始检查按钮
        email_check_finished_layout = QHBoxLayout()
        email_check_finished_layout.setContentsMargins(5, 5, 5, 5)
        self.email_check_finished_btn = QPushButton("保存标记结果")
        self.email_check_finished_btn.setFont(QFont('Microsoft YaHei', 15))
        self.email_check_finished_btn.setFixedHeight(40)

        # 二次检索按钮
        self.email_check_second_search_btn = QPushButton("二次检索")
        self.email_check_second_search_btn.setProperty('name', 'email_check_second_search_btn')
        self.email_check_second_search_btn.setFixedHeight(40)
        self.email_check_second_search_btn.setFixedWidth(100)
        email_check_second_search_btn_qss = '''QPushButton[name='email_check_second_search_btn']{background-color:rgb(0,255,255)}'''
        self.email_check_second_search_btn.setStyleSheet(email_check_second_search_btn_qss)
        email_check_finished_layout.addWidget(self.email_check_finished_btn)
        email_check_finished_layout.addWidget(self.email_check_second_search_btn)

        stack_email_check_w1 = QWidget()
        stack_email_check_w2 = QWidget()
        stack_email_check_w3 = QWidget()
        stack_email_check_w4 = QWidget()
        stack_email_check_w5 = QWidget()
        stack_email_check_w6 = QWidget()
        stack_email_check_w7 = QWidget()
        stack_email_check_w8 = QWidget()

        stack_email_check_w1.setLayout(email_check_login_layout)
        stack_email_check_w2.setLayout(email_check_protocol_type_layout)
        stack_email_check_w3.setLayout(email_check_start_check_layout)
        stack_email_check_w4.setLayout(email_check_check_result_layout)
        stack_email_check_w5.setLayout(email_check_check_result_table_layout)
        stack_email_check_w6.setLayout(email_check_check_pbar_layout)
        stack_email_check_w7.setLayout(email_check_end_search_btn_layout)
        stack_email_check_w8.setLayout(email_check_finished_layout)

        stack_email_check_layout = QVBoxLayout()
        stack_email_check_layout.setSpacing(0)
        stack_email_check_layout.addWidget(stack_email_check_w1)
        stack_email_check_layout.addWidget(stack_email_check_w2)
        stack_email_check_layout.addWidget(stack_email_check_w3)
        stack_email_check_layout.addWidget(stack_email_check_w4)
        stack_email_check_layout.addWidget(stack_email_check_w5)
        stack_email_check_layout.addWidget(stack_email_check_w6)
        stack_email_check_layout.addWidget(stack_email_check_w7)
        stack_email_check_layout.addWidget(stack_email_check_w8)
        self.stack_email_check.setLayout(stack_email_check_layout)

    # 处理函数
    def email_check_start_check_btn_handle(self):
        insert_op_record(self.current_user, "邮件检查")

    # 图片检查页面
    def stack_pic_check_UI(self):
        # 图片检查类型标签
        pic_check_type_layout = QHBoxLayout()
        pic_check_type_layout.setContentsMargins(5, 5, 5, 5)
        pic_check_type_label = QLabel("检查图片类型")
        pic_check_type_label.setFont(QFont('Microsoft YaHei', 12))
        self.pic_check_type_checkBox_jpg = QCheckBox(".JPG")
        self.pic_check_type_checkBox_jpg.setFont(QFont('Microsoft YaHei', 12))
        self.pic_check_type_checkBox_png = QCheckBox(".PNG")
        self.pic_check_type_checkBox_png.setFont(QFont('Microsoft YaHei', 12))
        # self.pic_check_type_checkBox_all = QCheckBox("全部类型")
        # self.pic_check_type_checkBox_all.setFont(QFont('Microsoft YaHei', 12))
        pic_check_type_layout.addWidget(pic_check_type_label)
        pic_check_type_layout.addWidget(self.pic_check_type_checkBox_jpg)
        pic_check_type_layout.addWidget(self.pic_check_type_checkBox_png)
        # pic_check_type_layout.addWidget(self.pic_check_type_checkBox_all)


        # 图片检查-开始检查
        pic_check_start_check_layout = QHBoxLayout()
        pic_check_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.pic_check_start_check_btn = QPushButton("开始检查")
        self.pic_check_start_check_btn.clicked.connect(self.pic_check_start_check_btn_handle)
        self.pic_check_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.pic_check_start_check_btn.setFixedHeight(60)
        pic_check_start_check_layout.addWidget(self.pic_check_start_check_btn)

        # 图片检查-检查结果
        pic_check_check_result_layout = QHBoxLayout()
        pic_check_check_result_layout.setContentsMargins(5, 5, 5, 5)
        pic_check_check_result_label = QLabel("检查结果")
        pic_check_check_result_label.setFont(QFont('Microsoft YaHei', 10))
        pic_check_check_result_layout.addStretch(1)
        pic_check_check_result_layout.addWidget(pic_check_check_result_label)
        pic_check_check_result_layout.addStretch(1)

        # 邮件检查-检查结果表格
        pic_check_check_result_table_layout = QHBoxLayout()
        pic_check_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.pic_check_check_result_table = QTableWidget()
        self.pic_check_check_result_table.setRowCount(100)  # 设置行数
        self.pic_check_check_result_table.setColumnCount(5)  # 设置列数
        self.pic_check_check_result_table.setHorizontalHeaderLabels(["IP端口", "图片名", "图片", "置信度等级", "选择涉密等级"])  # 设置表头
        self.pic_check_check_result_table.setColumnWidth(0, 100)  # 设置列宽
        self.pic_check_check_result_table.setColumnWidth(1, 200)
        self.pic_check_check_result_table.setColumnWidth(2, 200)
        self.pic_check_check_result_table.setColumnWidth(3, 200)
        self.pic_check_check_result_table.setColumnWidth(4, 180)
        self.pic_check_check_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        pic_check_check_result_table_layout.addWidget(self.pic_check_check_result_table)

        # 检查进度
        pic_check_check_pbar_layout = QHBoxLayout()
        pic_check_check_pbar_layout.setContentsMargins(5, 5, 5, 5)
        pic_check_check_pbar_label = QLabel("检查进度")
        pic_check_check_pbar_label.setFont(QFont('Microsoft YaHei', 15))
        self.pic_check_check_pbar = QProgressBar()
        self.pic_check_check_pbar.setValue(50)
        self.pic_check_check_pbar.setFixedHeight(30)
        pic_check_check_pbar_layout.addWidget(pic_check_check_pbar_label)
        pic_check_check_pbar_layout.addWidget(self.pic_check_check_pbar)

        # 终止检查按钮
        pic_check_end_search_btn_layout = QHBoxLayout()
        pic_check_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.pic_check_end_search_btn = QPushButton("终止检查")
        self.pic_check_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.pic_check_end_search_btn.setProperty('name', 'pic_check_end_search_btn')
        pic_end_search_btn_qss = '''QPushButton[name='pic_check_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.pic_check_end_search_btn.setStyleSheet(pic_end_search_btn_qss)
        self.pic_check_end_search_btn.setFixedHeight(40)
        pic_check_end_search_btn_layout.addWidget(self.pic_check_end_search_btn)

        # 选择完成，开始检查按钮
        pic_check_finished_layout = QHBoxLayout()
        pic_check_finished_layout.setContentsMargins(5, 5, 5, 5)
        self.pic_check_finished_btn = QPushButton("保存标记结果")
        self.pic_check_finished_btn.setFont(QFont('Microsoft YaHei', 15))
        self.pic_check_finished_btn.setFixedHeight(40)

        # 二次检索按钮
        self.pic_check_second_search_btn = QPushButton("二次检索")
        self.pic_check_second_search_btn.setProperty('name', 'pic_check_second_search_btn')
        self.pic_check_second_search_btn.setFixedHeight(40)
        self.pic_check_second_search_btn.setFixedWidth(100)
        pic_check_second_search_btn_qss = '''QPushButton[name='pic_check_second_search_btn']{background-color:rgb(0,255,255)}'''
        self.pic_check_second_search_btn.setStyleSheet(pic_check_second_search_btn_qss)
        pic_check_finished_layout.addWidget(self.pic_check_finished_btn)
        pic_check_finished_layout.addWidget(self.pic_check_second_search_btn)

        stack_pic_check_w1 = QWidget()
        stack_pic_check_w2 = QWidget()
        stack_pic_check_w3 = QWidget()
        stack_pic_check_w4 = QWidget()
        stack_pic_check_w5 = QWidget()
        stack_pic_check_w6 = QWidget()
        stack_pic_check_w7 = QWidget()

        stack_pic_check_w1.setLayout(pic_check_type_layout)
        stack_pic_check_w2.setLayout(pic_check_start_check_layout)
        stack_pic_check_w3.setLayout(pic_check_check_result_layout)
        stack_pic_check_w4.setLayout(pic_check_check_result_table_layout)
        stack_pic_check_w5.setLayout(pic_check_check_pbar_layout)
        stack_pic_check_w6.setLayout(pic_check_end_search_btn_layout)
        stack_pic_check_w7.setLayout(pic_check_finished_layout)

        stack_pic_check_layout = QVBoxLayout()
        stack_pic_check_layout.setSpacing(0)
        stack_pic_check_layout.addWidget(stack_pic_check_w1)
        stack_pic_check_layout.addWidget(stack_pic_check_w2)
        stack_pic_check_layout.addWidget(stack_pic_check_w3)
        stack_pic_check_layout.addWidget(stack_pic_check_w4)
        stack_pic_check_layout.addWidget(stack_pic_check_w5)
        stack_pic_check_layout.addWidget(stack_pic_check_w6)
        stack_pic_check_layout.addWidget(stack_pic_check_w7)

        self.stack_pic_check.setLayout(stack_pic_check_layout)

    # 处理函数
    def pic_check_start_check_btn_handle(self):
        insert_op_record(self.current_user, "图片检查")

    # 数据库日志检查页面
    def stack_db_log_check_UI(self):
        # 开始检查按钮
        db_log_check_start_check_layout = QHBoxLayout()
        db_log_check_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.db_log_check_start_check_btn = QPushButton("开始检查")
        self.db_log_check_start_check_btn.clicked.connect(self.db_log_check_start_check_btn_handle)
        self.db_log_check_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.db_log_check_start_check_btn.setFixedHeight(60)
        db_log_check_start_check_layout.addWidget(self.db_log_check_start_check_btn)

        # 数据库日志检查-检查结果
        db_logcheck_check_result_layout = QHBoxLayout()
        db_logcheck_check_result_layout.setContentsMargins(5, 5, 5, 5)
        db_logcheck_check_result_label = QLabel("检查结果")
        db_logcheck_check_result_label.setFont(QFont('Microsoft YaHei', 10))
        db_logcheck_check_result_layout.addStretch(1)
        db_logcheck_check_result_layout.addWidget(db_logcheck_check_result_label)
        db_logcheck_check_result_layout.addStretch(1)

        # 邮件检查-检查结果表格
        db_log_check_check_result_table_layout = QHBoxLayout()
        db_log_check_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.db_log_check_check_result_table = QTableWidget()
        self.db_log_check_check_result_table.setRowCount(100)  # 设置行数
        self.db_log_check_check_result_table.setColumnCount(4)  # 设置列数
        self.db_log_check_check_result_table.setHorizontalHeaderLabels(["IP端口", "操作", "文件名", "时间"])  # 设置表头
        self.db_log_check_check_result_table.setColumnWidth(0, 145)  # 设置列宽
        self.db_log_check_check_result_table.setColumnWidth(1, 250)
        self.db_log_check_check_result_table.setColumnWidth(2, 250)
        self.db_log_check_check_result_table.setColumnWidth(3, 250)
        self.db_log_check_check_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        db_log_check_check_result_table_layout.addWidget(self.db_log_check_check_result_table)

        # 检查进度
        db_log_check_check_pbar_layout = QHBoxLayout()
        db_log_check_check_pbar_layout.setContentsMargins(5, 5, 5, 5)
        db_log_check_check_pbar_label = QLabel("检查进度")
        db_log_check_check_pbar_label.setFont(QFont('Microsoft YaHei', 15))
        self.db_log_check_check_pbar = QProgressBar()
        self.db_log_check_check_pbar.setValue(50)
        self.db_log_check_check_pbar.setFixedHeight(30)
        db_log_check_check_pbar_layout.addWidget(db_log_check_check_pbar_label)
        db_log_check_check_pbar_layout.addWidget(self.db_log_check_check_pbar)

        # 终止检查按钮
        db_log_check_end_search_btn_layout = QHBoxLayout()
        db_log_check_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.db_log_check_end_search_btn = QPushButton("终止检查")
        self.db_log_check_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.db_log_check_end_search_btn.setProperty('name', 'db_log_check_end_search_btn')
        db_log_end_search_btn_qss = '''QPushButton[name='db_log_check_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.db_log_check_end_search_btn.setStyleSheet(db_log_end_search_btn_qss)
        self.db_log_check_end_search_btn.setFixedHeight(40)
        db_log_check_end_search_btn_layout.addWidget(self.db_log_check_end_search_btn)

        stack_db_log_check_w1 = QWidget()
        stack_db_log_check_w2 = QWidget()
        stack_db_log_check_w3 = QWidget()
        stack_db_log_check_w4 = QWidget()
        stack_db_log_check_w5 = QWidget()

        stack_db_log_check_w1.setLayout(db_log_check_start_check_layout)
        stack_db_log_check_w2.setLayout(db_logcheck_check_result_layout)
        stack_db_log_check_w3.setLayout(db_log_check_check_result_table_layout)
        stack_db_log_check_w4.setLayout(db_log_check_check_pbar_layout)
        stack_db_log_check_w5.setLayout(db_log_check_end_search_btn_layout)

        stack_db_log_check_layout = QVBoxLayout(self)
        stack_db_log_check_layout.addWidget(stack_db_log_check_w1)
        stack_db_log_check_layout.addWidget(stack_db_log_check_w2)
        stack_db_log_check_layout.addWidget(stack_db_log_check_w3)
        stack_db_log_check_layout.addWidget(stack_db_log_check_w4)
        stack_db_log_check_layout.addWidget(stack_db_log_check_w5)

        self.stack_db_log_check.setLayout(stack_db_log_check_layout)

    # 处理函数
    def db_log_check_start_check_btn_handle(self):
        insert_op_record(self.current_user, "数据库日志检查")

    # 数据库安全扫描页面
    def stack_security_scan_UI(self):
        # 开始检查按钮
        security_scan_start_check_layout = QHBoxLayout()
        security_scan_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.security_scan_start_check_btn = QPushButton("开始检查")
        self.security_scan_start_check_btn.clicked.connect(self.security_scan_start_check_btn_handle)
        self.security_scan_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.security_scan_start_check_btn.setFixedHeight(60)
        security_scan_start_check_layout.addWidget(self.security_scan_start_check_btn)

        # 数据库安全扫描-检查结果
        security_scan_result_layout = QHBoxLayout()
        security_scan_result_layout.setContentsMargins(5, 5, 5, 5)
        security_scan_result_layout_result_label = QLabel("检查结果")
        security_scan_result_layout_result_label.setFont(QFont('Microsoft YaHei', 10))
        security_scan_result_layout.addStretch(1)
        security_scan_result_layout.addWidget(security_scan_result_layout_result_label)
        security_scan_result_layout.addStretch(1)

        # 检查结果表格
        security_scan_result_table_layout = QHBoxLayout()
        security_scan_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.security_scan_result_table = QTableWidget()
        self.security_scan_result_table.setRowCount(100)  # 设置行数
        self.security_scan_result_table.setColumnCount(4)  # 设置列数
        self.security_scan_result_table.setHorizontalHeaderLabels(["IP端口", "用户列表", "弱口令", "权限"])  # 设置表头
        self.security_scan_result_table.setColumnWidth(0, 140)  # 设置列宽
        self.security_scan_result_table.setColumnWidth(1, 250)
        self.security_scan_result_table.setColumnWidth(2, 250)
        self.security_scan_result_table.setColumnWidth(3, 250)
        self.security_scan_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        security_scan_result_table_layout.addWidget(self.security_scan_result_table)

        # 检查进度
        security_scan_pbar_layout = QHBoxLayout()
        security_scan_pbar_layout.setContentsMargins(5, 5, 5, 5)
        security_scan_pbar_label = QLabel("检查进度")
        security_scan_pbar_label.setFont(QFont('Microsoft YaHei', 15))
        self.security_scan_pbar = QProgressBar()
        self.security_scan_pbar.setValue(50)
        self.security_scan_pbar.setFixedHeight(30)
        security_scan_pbar_layout.addWidget(security_scan_pbar_label)
        security_scan_pbar_layout.addWidget(self.security_scan_pbar)

        # 终止检查按钮
        security_scan_end_search_btn_layout = QHBoxLayout()
        security_scan_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.security_scan_end_search_btn = QPushButton("终止检查")
        self.security_scan_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.security_scan_end_search_btn.setProperty('name', 'security_scan_end_search_btn')
        security_scan_end_search_btn_qss = '''QPushButton[name='security_scan_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.security_scan_end_search_btn.setStyleSheet(security_scan_end_search_btn_qss)
        self.security_scan_end_search_btn.setFixedHeight(40)
        security_scan_end_search_btn_layout.addWidget(self.security_scan_end_search_btn)

        stack_security_scan_check_w1 = QWidget()
        stack_security_scan_check_w2 = QWidget()
        stack_security_scan_check_w3 = QWidget()
        stack_security_scan_check_w4 = QWidget()
        stack_security_scan_check_w5 = QWidget()

        stack_security_scan_check_w1.setLayout(security_scan_start_check_layout)
        stack_security_scan_check_w2.setLayout(security_scan_result_layout)
        stack_security_scan_check_w3.setLayout(security_scan_result_table_layout)
        stack_security_scan_check_w4.setLayout(security_scan_pbar_layout)
        stack_security_scan_check_w5.setLayout(security_scan_end_search_btn_layout)

        stack_stack_security_check_layout = QVBoxLayout(self)
        stack_stack_security_check_layout.addWidget(stack_security_scan_check_w1)
        stack_stack_security_check_layout.addWidget(stack_security_scan_check_w2)
        stack_stack_security_check_layout.addWidget(stack_security_scan_check_w3)
        stack_stack_security_check_layout.addWidget(stack_security_scan_check_w4)
        stack_stack_security_check_layout.addWidget(stack_security_scan_check_w5)

        self.stack_security_scan.setLayout(stack_stack_security_check_layout)

    # 处理函数
    def security_scan_start_check_btn_handle(self):
        insert_op_record(self.current_user, "数据库安全扫描")

    # 二次检索页面
    def stack_second_check_UI(self):
        # 二次检索-按照涉密等级划分
        second_check_class_layout = QHBoxLayout()
        second_check_class_layout.setContentsMargins(5, 5, 5, 5)
        second_check_class_label = QLabel("按照涉密等级检索")
        second_check_class_label.setFont(QFont('Microsoft YaHei', 12))

        self.second_check_class_comboBox = QComboBox()
        self.second_check_class_comboBox.addItems(["可疑"])
        self.second_check_class_comboBox.setFixedHeight(30)
        self.second_check_class_comboBox.setFixedWidth(700)
        second_check_class_layout.addWidget(second_check_class_label)
        second_check_class_layout.addWidget(self.second_check_class_comboBox)
        second_check_class_layout.addSpacing(50)

        # 二次检索-按照文件类型划分
        second_check_filetype_layout = QHBoxLayout()
        second_check_filetype_layout.setContentsMargins(5, 5, 5, 5)
        second_check_filetype_label = QLabel("按照文件类型检索")
        second_check_filetype_label.setFont(QFont('Microsoft YaHei', 12))
        self.second_check_filetype_comboBox = QComboBox()
        self.second_check_filetype_comboBox.setFixedHeight(30)
        self.second_check_filetype_comboBox.setFixedWidth(700)
        self.second_check_filetype_comboBox.addItems(["PDF"])
        self.second_check_filetype_comboBox.addItems(["TXT"])
        second_check_filetype_layout.addWidget(second_check_filetype_label)
        second_check_filetype_layout.addWidget(self.second_check_filetype_comboBox)
        second_check_filetype_layout.addSpacing(50)

        # 二次检索-按照关键词划分
        second_check_keyword_layout = QHBoxLayout()
        second_check_keyword_layout.setContentsMargins(5, 5, 5, 5)
        second_check_keyword_label = QLabel("按照关键词检索")
        second_check_keyword_label.setFont(QFont('Microsoft YaHei', 12))
        self.second_check_keyword_comboBox = QComboBox()
        self.second_check_keyword_comboBox.setFixedHeight(30)
        self.second_check_keyword_comboBox.setFixedWidth(700)
        self.second_check_keyword_comboBox.addItems(["身份证"])
        self.second_check_keyword_comboBox.addItems(["坦克"])
        second_check_keyword_layout.addWidget(second_check_keyword_label)
        second_check_keyword_layout.addWidget(self.second_check_keyword_comboBox)
        second_check_keyword_layout.addSpacing(50)

        # 二次检索-开始检查按钮
        second_check_start_check_layout = QHBoxLayout()
        second_check_start_check_layout.setContentsMargins(5, 5, 5, 5)
        self.second_check_start_check_btn = QPushButton("开始检查")
        self.second_check_start_check_btn.clicked.connect(self.second_check_start_check_btn_handle)
        self.second_check_start_check_btn.setFont(QFont('Microsoft YaHei', 15))
        self.second_check_start_check_btn.setFixedHeight(40)
        second_check_start_check_layout.addWidget(self.second_check_start_check_btn)

        # 二次检索-检查结果
        second_check_result_layout = QHBoxLayout()
        second_check_result_layout.setContentsMargins(5, 5, 5, 5)
        second_check_result_layout_result_label = QLabel("检查结果")
        second_check_result_layout_result_label.setFont(QFont('Microsoft YaHei', 10))
        second_check_result_layout.addStretch(1)
        second_check_result_layout.addWidget(second_check_result_layout_result_label)
        second_check_result_layout.addStretch(1)

        # 二次检查-检查结果表格
        second_check_result_table_layout = QHBoxLayout()
        second_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.second_check_result_table = QTableWidget()
        self.second_check_result_table.setRowCount(100)  # 设置行数
        self.second_check_result_table.setColumnCount(4)  # 设置列数
        self.second_check_result_table.setHorizontalHeaderLabels(["IP端口", "文件类型", "文件名", "涉密等级"])  # 设置表头
        self.second_check_result_table.setColumnWidth(0, 150)  # 设置列宽
        self.second_check_result_table.setColumnWidth(1, 250)
        self.second_check_result_table.setColumnWidth(2, 250)
        self.second_check_result_table.setColumnWidth(3, 250)
        self.second_check_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        second_check_result_table_layout.addWidget(self.second_check_result_table)

        # 检查进度
        second_check_pbar_layout = QHBoxLayout()
        second_check_pbar_layout.setContentsMargins(5, 5, 5, 5)
        second_check_pbar_label = QLabel("检查进度")
        second_check_pbar_label.setFont(QFont('Microsoft YaHei', 15))
        self.second_check_pbar = QProgressBar()
        self.second_check_pbar.setValue(50)
        self.second_check_pbar.setFixedHeight(30)
        second_check_pbar_layout.addWidget(second_check_pbar_label)
        second_check_pbar_layout.addWidget(self.second_check_pbar)

        # 终止检查按钮
        second_check_end_search_btn_layout = QHBoxLayout()
        second_check_end_search_btn_layout.setContentsMargins(5, 5, 5, 5)
        self.second_check_end_search_btn = QPushButton("终止检查")
        self.second_check_end_search_btn.setFont(QFont('Microsoft YaHei', 15))
        self.second_check_end_search_btn.setProperty('name', 'second_check_end_search_btn')
        second_check_end_search_btn_qss = '''QPushButton[name='second_check_end_search_btn']{background-color:rgb(255,0,0)}'''
        self.second_check_end_search_btn.setStyleSheet(second_check_end_search_btn_qss)
        self.second_check_end_search_btn.setFixedHeight(40)
        second_check_end_search_btn_layout.addWidget(self.second_check_end_search_btn)

        stack_second_check_check_w1 = QWidget()
        stack_second_check_check_w2 = QWidget()
        stack_second_check_check_w3 = QWidget()
        stack_second_check_check_w4 = QWidget()
        stack_second_check_check_w5 = QWidget()
        stack_second_check_check_w6 = QWidget()
        stack_second_check_check_w7 = QWidget()
        stack_second_check_check_w8 = QWidget()

        stack_second_check_check_w1.setLayout(second_check_class_layout)
        stack_second_check_check_w2.setLayout(second_check_filetype_layout)
        stack_second_check_check_w3.setLayout(second_check_keyword_layout)
        stack_second_check_check_w4.setLayout(second_check_start_check_layout)
        stack_second_check_check_w5.setLayout(second_check_result_layout)
        stack_second_check_check_w6.setLayout(second_check_result_table_layout)
        stack_second_check_check_w7.setLayout(second_check_pbar_layout)
        stack_second_check_check_w8.setLayout(second_check_end_search_btn_layout)

        stack_second_check_check_layout = QVBoxLayout(self)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w1)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w2)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w3)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w4)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w5)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w6)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w7)
        stack_second_check_check_layout.addWidget(stack_second_check_check_w8)

        self.stack_second_check.setLayout(stack_second_check_check_layout)

    # 处理函数
    def second_check_start_check_btn_handle(self):
        insert_op_record(self.current_user, "二次检索")

    # 检查结果页面
    def stack_result_UI(self):
        # 文件检查结果
        file_check_result_layout = QHBoxLayout()
        file_check_result_layout.setContentsMargins(5, 5, 5, 5)
        file_check_result_label = QLabel("文件检查结果")
        file_check_result_label.setFont(QFont('Microsoft YaHei', 12))
        file_check_result_layout.addStretch(1)
        file_check_result_layout.addWidget(file_check_result_label)
        file_check_result_layout.addStretch(1)
        # 文件检查结果表格
        file_check_result_table_layout = QHBoxLayout()
        file_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.file_check_result_table = QTableWidget()
        self.file_check_result_table.setRowCount(100)
        self.file_check_result_table.setColumnCount(3)
        self.file_check_result_table.setHorizontalHeaderLabels(["IP端口", "文件检查数量", "可疑文件数量"])  # 设置表头
        self.file_check_result_table.setColumnWidth(0, 297)
        self.file_check_result_table.setColumnWidth(1, 297)
        self.file_check_result_table.setColumnWidth(2, 297)
        file_check_result_table_layout.addWidget(self.file_check_result_table)

        # 邮件检查结果
        email_check_result_layout = QHBoxLayout()
        email_check_result_layout.setContentsMargins(5, 5, 5, 5)
        email_check_result_label = QLabel("邮件检查结果")
        email_check_result_label.setFont(QFont('Microsoft YaHei', 12))
        email_check_result_layout.addStretch(1)
        email_check_result_layout.addWidget(email_check_result_label)
        email_check_result_layout.addStretch(1)
        # 邮件检查结果表格
        email_check_result_table_layout = QHBoxLayout()
        email_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.email_check_result_table = QTableWidget()
        self.email_check_result_table.setRowCount(100)
        self.email_check_result_table.setColumnCount(3)
        self.email_check_result_table.setHorizontalHeaderLabels(["类型", "文件检查数量", "可疑文件数量"])  # 设置表头
        self.email_check_result_table.setColumnWidth(0, 297)
        self.email_check_result_table.setColumnWidth(1, 297)
        self.email_check_result_table.setColumnWidth(2, 297)
        email_check_result_table_layout.addWidget(self.email_check_result_table)

        # 图片检查结果
        pic_check_result_layout = QHBoxLayout()
        pic_check_result_layout.setContentsMargins(5, 5, 5, 5)
        pic_check_result_label = QLabel("图片检查结果")
        pic_check_result_label.setFont(QFont('Microsoft YaHei', 12))
        pic_check_result_layout.addStretch(1)
        pic_check_result_layout.addWidget(pic_check_result_label)
        pic_check_result_layout.addStretch(1)
        # 图片检查结果表格
        pic_check_result_table_layout = QHBoxLayout()
        pic_check_result_table_layout.setContentsMargins(5, 5, 5, 5)
        self.pic_check_result_table = QTableWidget()
        self.pic_check_result_table.setRowCount(100)
        self.pic_check_result_table.setColumnCount(3)
        self.pic_check_result_table.setHorizontalHeaderLabels(["类型", "文件检查数量", "可疑文件数量"])  # 设置表头
        self.pic_check_result_table.setColumnWidth(0, 297)
        self.pic_check_result_table.setColumnWidth(1, 297)
        self.pic_check_result_table.setColumnWidth(2, 297)
        pic_check_result_table_layout.addWidget(self.pic_check_result_table)

        stack_result_w1 = QWidget()
        stack_result_w2 = QWidget()
        stack_result_w3 = QWidget()
        stack_result_w4 = QWidget()
        stack_result_w5 = QWidget()
        stack_result_w6 = QWidget()

        stack_result_w1.setLayout(file_check_result_layout)
        stack_result_w2.setLayout(file_check_result_table_layout)
        stack_result_w3.setLayout(email_check_result_layout)
        stack_result_w4.setLayout(email_check_result_table_layout)
        stack_result_w5.setLayout(pic_check_result_layout)
        stack_result_w6.setLayout(pic_check_result_table_layout)

        stack_result_layout = QVBoxLayout(self)
        stack_result_layout.setSpacing(0)
        stack_result_layout.addWidget(stack_result_w1)
        stack_result_layout.addWidget(stack_result_w2)
        stack_result_layout.addWidget(stack_result_w3)
        stack_result_layout.addWidget(stack_result_w4)
        stack_result_layout.addWidget(stack_result_w5)
        stack_result_layout.addWidget(stack_result_w6)

        self.stack_result.setLayout(stack_result_layout)

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
    main_win = MainWin()
    main_win.show()
    sys.exit(app.exec())

