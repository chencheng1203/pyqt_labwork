# -*- encoding:utf-8 -*-
# @Time: 2020/1/1 10:46


import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QDesktopWidget, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
import PyQt5.QtCore as QtCore
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel  # 数据库
from MainWindow import MainWin
from Checker_Window import Checker_Win
from login_state_dialog import sucess_login, failed_login_not_input, failed_login_passwd_error
from utils import insert_user, search_all_user_account, search_user


class LoginWin(QDialog):
    def __init__(self):
        self.mainWin = MainWin() # 主窗口
        self.checker_Win = Checker_Win()
        self.sucess_login_message = sucess_login()  # 登录状态提示
        self.failed_login_not_input = failed_login_not_input()  # 登录状态提示
        self.failed_login_passwd_error = failed_login_passwd_error()  # 登录状态提示

        super(LoginWin, self).__init__()

        # 页面初始化
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"./images/软件图标.ico"))
        self.resize(1200, 800)
        self.center()
        self.setFixedSize(self.width(), self.height())

        win_palette = QPalette()  # 设置窗口样式
        win_palette.setBrush(QPalette.Background, QBrush(QPixmap('./images/bg_4.jpg')))
        self.setPalette(win_palette)

        # 标题
        title_layout = QHBoxLayout()
        icon_title = QLabel(self)
        icon_title.setPixmap(QPixmap('./images/数据库维护服务.png'))
        title_label = QLabel("数据库检查系统", self)
        title_label.setFont(QFont('Ink Free', 25))
        title_layout.addStretch(4)
        title_layout.addWidget(icon_title)
        title_layout.addStretch(0)
        title_layout.addWidget(title_label)
        title_layout.addStretch(4)

        # 欢迎登录
        welcome_label = QLabel("欢迎登录", self)
        welcome_label.setFont(QFont('Ink Free', 20))
        welcome_layout = QHBoxLayout()
        welcome_layout.addStretch(2)
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addStretch(2)

        # 用户名
        user_name_layout = QHBoxLayout()
        user_name_label = QLabel("用户名", self)
        user_name_label.setFont(QFont('Microsoft YaHei', 15))
        self.user_name_edit = QLineEdit("", self)
        self.user_name_edit.setMinimumSize(300, 40)
        self.user_name_edit.setMaximumSize(300, 40)
        user_name_layout.addSpacing(400)
        user_name_layout.addWidget(user_name_label)
        user_name_layout.addWidget(self.user_name_edit)
        user_name_layout.addSpacing(400)

        # 密码
        passwd_layout = QHBoxLayout()
        passwd_label = QLabel("   密码")
        passwd_label.setFont(QFont('Microsoft YaHei', 15))
        self.passwd_edit = QLineEdit("")
        self.passwd_edit.setEchoMode(QLineEdit.Password)
        self.passwd_edit.setMinimumSize(300, 40)
        self.passwd_edit.setMaximumSize(300, 40)
        passwd_layout.addSpacing(400)
        passwd_layout.addWidget(passwd_label)
        passwd_layout.addWidget(self.passwd_edit)
        passwd_layout.addSpacing(400)

        # 用户类型选项
        user_class_layout = QHBoxLayout()
        self.user_baomiyuan = QRadioButton("保密员", self)
        self.user_baomiyuan.setChecked(True)  # 默认保密员账号登录
        self.user_baomiyuan.setFont(QFont('Microsoft YaHei', 15))
        self.user_shenchayuan = QRadioButton("审查员", self)
        self.user_shenchayuan.setFont(QFont('Microsoft YaHei', 15))
        user_class_layout.addStretch(3)
        user_class_layout.addWidget(self.user_baomiyuan)
        user_class_layout.addSpacing(100)
        user_class_layout.addWidget((self.user_shenchayuan))
        user_class_layout.addStretch(3)

        # 登录按钮
        self.login_button = QPushButton("立即登录", self)
        self.login_button.setFont(QFont('Segoe Print', 15))
        self.login_button.setMinimumSize(400, 50)
        self.login_button.setMaximumSize(400, 50)
        self.login_button.clicked.connect(self.handle_login_btn)
        login_layout = QHBoxLayout()
        # login_layout.addStretch(1)
        login_layout.addSpacing(350)
        login_layout.addWidget(self.login_button)
        login_layout.addSpacing(350)
        # login_layout.addStretch(1)

        # 忘记密码
        forget_passwd_label = QLabel("忘记密码？请联系管理员")
        forget_passwd_label.setFont(QFont('Microsoft YaHei', 10))
        forget_passwd_layout = QHBoxLayout()
        forget_passwd_layout.addSpacing(350)
        forget_passwd_layout.addWidget(forget_passwd_label)

        # 全局布局设置
        all_layout = QVBoxLayout()
        title_widget = QWidget(self)
        user_name_widget = QWidget(self)
        passwd_widget = QWidget(self)
        welcome_widget = QWidget(self)
        user_class_widget = QWidget(self)
        login_button_widget = QWidget(self)
        forget_passwd_widget = QWidget(self)

        title_widget.setLayout(title_layout)
        user_name_widget.setLayout(user_name_layout)
        passwd_widget.setLayout(passwd_layout)
        welcome_widget.setLayout(welcome_layout)
        user_class_widget.setLayout(user_class_layout)
        login_button_widget.setLayout(login_layout)
        forget_passwd_widget.setLayout(forget_passwd_layout)

        all_layout.addSpacing(170)
        all_layout.addWidget(title_widget)
        all_layout.addWidget(welcome_widget)
        all_layout.addWidget(user_name_widget)
        all_layout.addWidget(passwd_widget)
        all_layout.addWidget(user_class_widget)
        all_layout.addWidget(login_button_widget)
        all_layout.addWidget(forget_passwd_widget)
        all_layout.addSpacing(100)
        self.setLayout(all_layout)

    # 引入数据库之后的登录操作
    def handle_login_btn(self):
        user_name = str(self.user_name_edit.text())
        passwd = str(self.passwd_edit.text())
        if self.user_baomiyuan.isChecked():
            state = search_user(user_name, passwd)
            print(state)
            print('----------')
            if state[1] == 1:
                self.sucess_login_message.show()
                self.mainWin.show()
                self.close()
            elif self.user_name_edit.text() == '' or self.passwd_edit.text() == '':
                QApplication.setQuitOnLastWindowClosed(False)
                self.failed_login_not_input.show()
            elif state[0] == 1 and state[1] != 1:  # 密码错误
                self.failed_login_passwd_error.show()
        else:
            self.checker_Win.show()
            self.close()

    def closeEvent(self, QCloseEvent):
        # 关闭数据库
        pass

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_win = LoginWin()
    login_win.show()
    sys.exit(app.exec())
