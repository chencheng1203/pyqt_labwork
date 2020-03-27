# -*- encoding:utf-8 -*-
# @Time: 2020/2/21 7:39

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QCheckBox, \
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QProgressBar,\
    QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QAbstractItemView, \
    QDesktopWidget, QStackedWidget, QComboBox, QTextEdit, QHeaderView
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
from utils import get_current_time, read_data_from_keyword_dic_table
import PyQt5.QtCore as QtCore
import pymysql

# 创建关键词库字典
doc = read_data_from_keyword_dic_table()
keyword_title_dic = {}
for i, keyword in enumerate(doc):
    keyword_title_dic["keyword" + str(i + 1)] = keyword


# 查看数据
def show_data(keyword):
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",password="cc120323",
        database="info_manager_sys",
        charset="utf8")
    cursor = conn.cursor()
    sql = "select * from {}".format(keyword)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# 一开始显示的内容
ori_show_data_context = ""
data = show_data("keyword" + str(1))
for keyword_pair in data:
    ori_show_data_context += (keyword_pair[1] + " ")


class KeywordLib_Dialog(QWidget):
    def __init__(self):
        super(KeywordLib_Dialog, self).__init__()
        # 主界面控件初始化
        self.keyword_config_MainWin = QWidget()
        # 关键词库下标初始化
        self.choose_which_keyword_to_delete_table_index = 0
        # 数据表check记录
        self.delete_check = []
        # 页面初始化
        self.initUI()
        self.initLayout()
        # 表格初始化
        datas = show_data("keyword" + str(1))
        for data in datas:
            self.add_line(data[0], data[1])

    def initUI(self):
        self.setWindowTitle('数据库检查系统')  # 设置窗口名称
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
        self.info_box_layout = QHBoxLayout()
        self.info_box = QLineEdit(self)
        self.info_box.setReadOnly(True)  # 设置为只读
        self.info_box.setAlignment(Qt.AlignCenter)
        self.info_box.setWindowFlag(Qt.FramelessWindowHint)  # 无边框
        self.info_box.setFixedHeight(30)
        self.info_box_layout.setContentsMargins(0, 0, 0, 0)
        self.info_box_layout.addWidget(self.info_box)
        # 设置信息栏信息
        self.Timer = QTimer()
        self.Timer.start(500)
        self.Timer.timeout.connect(self.updateTime)

        # 关键词配置标题
        self.keyword_lable_layout = QHBoxLayout()
        self.keyword_lable_layout.setContentsMargins(2, 2, 2, 2)
        self.keyword_lable = QLabel("关键词配置")
        self.keyword_lable.setFont(QFont('Microsoft YaHei', 16))
        self.keyword_lable_layout.addStretch(1)
        self.keyword_lable_layout.addWidget(self.keyword_lable)
        self.keyword_lable_layout.addStretch(1)

        self.keyword_config_MainWin_UI()

    def keyword_config_MainWin_UI(self):
        # 选择要查看的关键词库
        choose_keyword_lib_layout = QHBoxLayout()
        choose_keyword_lib_layout.setContentsMargins(0, 0, 0, 0)
        choose_keyword_lib_lable = QLabel('选择要查看的关键词库')
        choose_keyword_lib_lable.setFont(QFont('Microsoft YaHei', 15))
        self.choose_keyword_lib_combox = QComboBox()
        self.choose_keyword_lib_combox.setFixedHeight(40)
        self.choose_keyword_lib_combox.setFixedWidth(500)

        choose_keyword_lib_comboxdata_items = []
        for keyword_content in keyword_title_dic.values():
            choose_keyword_lib_comboxdata_items.append(keyword_content)
        self.choose_keyword_lib_combox.addItems(choose_keyword_lib_comboxdata_items)
        # 当选择改变时的槽函数
        self.choose_keyword_lib_combox.currentIndexChanged.connect(self.keyword_lib_context)
        choose_keyword_lib_layout.addSpacing(75)
        choose_keyword_lib_layout.addWidget(choose_keyword_lib_lable)
        choose_keyword_lib_layout.addSpacing(10)
        choose_keyword_lib_layout.addWidget(self.choose_keyword_lib_combox)
        choose_keyword_lib_layout.addSpacing(400)

        # 关键词库内容标签
        keyword_lib_context_lable_layout = QHBoxLayout()
        keyword_lib_context_lable_layout.setContentsMargins(0, 0, 0, 0)
        keyword_lib_context_lable = QLabel('关键词库内容')
        keyword_lib_context_lable.setFont(QFont('Microsoft YaHei', 15))
        keyword_lib_context_lable_layout.addStretch(1)
        keyword_lib_context_lable_layout.addWidget(keyword_lib_context_lable)
        keyword_lib_context_lable_layout.addStretch(1)

        # 关键词库内容文本框
        keyword_lib_context_box_layout = QHBoxLayout()
        keyword_lib_context_box_layout.setContentsMargins(2, 2, 2, 2)
        self.keyword_lib_context_box = QTextEdit()
        # 显示初始化
        self.keyword_lib_context_box.setText(ori_show_data_context)
        self.keyword_lib_context_box.setFocusPolicy(QtCore.Qt.NoFocus)  # 设置不可编辑
        self.keyword_lib_context_box.setFixedWidth(1100)
        self.keyword_lib_context_box.setFixedHeight(130)
        keyword_lib_context_box_layout.addWidget(self.keyword_lib_context_box)

        # 选择要删除的关键词库字段
        choose_which_keyword_to_delete_layout = QHBoxLayout()
        choose_which_keyword_to_delete_layout.setContentsMargins(0, 0, 0, 0)
        choose_which_keyword_to_delete_label= QLabel('选择要删除的关键词库字段')
        choose_which_keyword_to_delete_label.setFont(QFont('Microsoft YaHei', 15))
        self.choose_which_keyword_to_delete_combox= QComboBox()
        self.choose_which_keyword_to_delete_combox.setFixedHeight(40)
        self.choose_which_keyword_to_delete_combox.setFixedWidth(500)
        self.choose_which_keyword_to_delete_combox.addItems(choose_keyword_lib_comboxdata_items)
        self.choose_which_keyword_to_delete_combox.currentIndexChanged.connect(self.add_data_to_table)
        choose_which_keyword_to_delete_layout.addSpacing(30)
        choose_which_keyword_to_delete_layout.addWidget(choose_which_keyword_to_delete_label)
        choose_which_keyword_to_delete_layout.addSpacing(10)
        choose_which_keyword_to_delete_layout.addWidget(self.choose_which_keyword_to_delete_combox)
        choose_which_keyword_to_delete_layout.addSpacing(500)

        # 关键词库表
        keyword_lib_table_layout = QHBoxLayout()
        keyword_lib_table_layout.setContentsMargins(0, 0, 0, 0)
        self.choose_which_keyword_to_delete_delete_btn = QPushButton("删除")
        self.choose_which_keyword_to_delete_delete_btn.clicked.connect(self.delete_selected_data)
        self.choose_which_keyword_to_delete_delete_btn.setFixedHeight(100)
        self.choose_which_keyword_to_delete_delete_btn.setFixedWidth(100)
        self.choose_which_keyword_to_delete_delete_btn.setProperty('name', 'choose_which_keyword_to_delete_delete_btn')
        choose_which_keyword_to_delete_delete_btn_qss = '''QPushButton[name='choose_which_keyword_to_delete_delete_btn']{background-color:rgb(255,0,0)}'''
        self.choose_which_keyword_to_delete_delete_btn.setStyleSheet(choose_which_keyword_to_delete_delete_btn_qss)
        self.keyword_lib_table = QTableWidget()
        self.keyword_lib_table.verticalHeader().hide()  # 隐藏行头
        self.keyword_lib_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.keyword_lib_table.setColumnCount(3)
        self.keyword_lib_table.setHorizontalHeaderLabels(["关键词序号", "关键词", "是否删除"])  # 设置表头
        self.keyword_lib_table.setColumnWidth(0, 100)
        self.keyword_lib_table.setColumnWidth(1, 440)
        self.keyword_lib_table.setColumnWidth(2, 500)
        self.keyword_lib_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        keyword_lib_table_layout.addWidget(self.keyword_lib_table)
        keyword_lib_table_layout.addWidget(self.choose_which_keyword_to_delete_delete_btn)

        # 保存配置
        save_config_btn_layout = QHBoxLayout()
        save_config_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.save_config_btn = QPushButton("保存配置")
        self.save_config_btn.clicked.connect(self.return_keyword_config_btn_handle)
        self.save_config_btn.setFont(QFont('Microsoft YaHei', 15))
        self.save_config_btn.setFixedHeight(40)

        # 返回关键词配置
        self.return_keyword_config_btn = QPushButton("未保存")
        self.return_keyword_config_btn.setProperty('name', 'return_keyword_config_btn')
        self.return_keyword_config_btn.setFixedHeight(40)
        self.return_keyword_config_btn.setFixedWidth(200)
        return_keyword_config_btn_qss = '''QPushButton[name='return_keyword_config_btn']{background-color:rgb(0,255,0)}'''
        self.return_keyword_config_btn.setStyleSheet(return_keyword_config_btn_qss)
        save_config_btn_layout.addWidget(self.save_config_btn)
        save_config_btn_layout.addWidget(self.return_keyword_config_btn)

        # 页面管理
        keyword_config_MainWin_w1 = QWidget()
        keyword_config_MainWin_w2 = QWidget()
        keyword_config_MainWin_w3 = QWidget()
        keyword_config_MainWin_w4 = QWidget()
        keyword_config_MainWin_w5 = QWidget()
        keyword_config_MainWin_w6 = QWidget()

        keyword_config_MainWin_w1.setLayout(choose_keyword_lib_layout)
        keyword_config_MainWin_w2.setLayout(keyword_lib_context_lable_layout)
        keyword_config_MainWin_w3.setLayout(keyword_lib_context_box_layout)
        keyword_config_MainWin_w4.setLayout(choose_which_keyword_to_delete_layout)
        keyword_config_MainWin_w5.setLayout(keyword_lib_table_layout)
        keyword_config_MainWin_w6.setLayout(save_config_btn_layout)

        # 总体布局
        keyword_config_MainWin_layout = QVBoxLayout()
        keyword_config_MainWin_layout.setContentsMargins(0, 0, 0, 0)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w1)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w2)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w3)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w4)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w5)
        keyword_config_MainWin_layout.addWidget(keyword_config_MainWin_w6)

        self.keyword_config_MainWin.setLayout(keyword_config_MainWin_layout)

    # 表格增加一行数据
    def add_line(self, num, keyword):
        row = self.keyword_lib_table.rowCount()
        self.keyword_lib_table.setRowCount(row + 1)
        # 下面六行用于生成居中的checkbox，不知道有没有别的好方法
        ck = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        self.keyword_lib_table.setItem(row, 0, QTableWidgetItem(str(num)))
        self.keyword_lib_table.setItem(row, 1, QTableWidgetItem(keyword))
        self.keyword_lib_table.setCellWidget(row, 2, w)
        self.delete_check.append(ck)

    # 增加多行数据
    def add_data_to_table(self, i):
        self.choose_which_keyword_to_delete_table_index = (i + 1)
        # 清空数据表check记录
        self.delete_check = []
        self.keyword_lib_table.setRowCount(0)  # 清空数据
        datas = show_data("keyword" + str(i + 1))
        for data in datas:
            self.add_line(data[0], data[1])

    # 表格删除数据函数
    def delete_selected_data(self):
        datas = show_data("keyword" + str(self.choose_which_keyword_to_delete_table_index))
        # 获取当前数据表
        index = self.choose_which_keyword_to_delete_combox.currentIndex()
        current_keyword = "keyword" + str(index + 1)
        conn = pymysql.connect(
            host="127.0.0.1",
            user="root", password="cc120323",
            database="info_manager_sys",
            charset="utf8")
        cursor = conn.cursor()
        for i, line_check in enumerate(self.delete_check):
            if line_check.isChecked():  # 如果被选中
                print("into")
                delete_sql = "delete from {} where keyword='{}'".format(current_keyword, datas[i][1])
                print(delete_sql)
                state_flag = cursor.execute(delete_sql)
                conn.commit()  # 提交操作
                print(state_flag)
        cursor.close()
        conn.close()
        # 更新显示
        self.keyword_lib_table.setRowCount(0)  # 清空数据
        datas = show_data("keyword" + str(index + 1))
        for data in datas:
            self.add_line(data[0], data[1])

    """
    返回关键词配置槽函数
    """
    def return_keyword_config_btn_handle(self):
        self.return_keyword_config_btn.setText("已保存")

    """
    关键词内容槽函数
    """
    def keyword_lib_context(self, i):
        show_data_context = ""
        data = show_data("keyword" + str(i + 1))
        for keyword_pair in data:
            show_data_context += (keyword_pair[1] + " ")
        self.keyword_lib_context_box.setText(show_data_context)

    def initLayout(self):
        # 全局布局设置
        all_layout = QVBoxLayout()
        title_widget = QWidget()
        info_widget = QWidget()
        keyword_lable_widget = QWidget()
        # keyword_config_MainWin_widget = QWidget()


        title_widget.setLayout(self.title_layout)
        info_widget.setLayout(self.info_box_layout)
        keyword_lable_widget.setLayout(self.keyword_lable_layout)
        # keyword_config_MainWin_widget.setLayout(self.keyword_config_MainWin_layout)

        all_layout.addWidget(title_widget)
        all_layout.addWidget(info_widget)
        all_layout.addWidget(keyword_lable_widget)
        all_layout.addWidget(self.keyword_config_MainWin)

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
    main_win = KeywordLib_Dialog()
    main_win.show()
    sys.exit(app.exec())
