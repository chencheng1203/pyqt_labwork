# -*- encoding:utf-8 -*-
# @Time: 2019/12/31 10:33


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont
import PyQt5.QtCore as QtCore


class LoginWin(QWidget):
    def __init__(self):
        super(LoginWin, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录')  # 设置窗口名称
        self.setWindowIcon(QIcon(r"./images/软件图标.ico"))
        self.resize(1200, 800)
        self.center()
        self.setFixedSize(self.width(), self.height())

        win_palette = QPalette()  # 设置窗口样式
        win_palette.setBrush(QPalette.Background, QBrush(QPixmap('./images/bg.jpg')))
        self.setPalette(win_palette)

        # 用户名密码
        user_passwd_layout = QFormLayout()
        user_name_label = QLabel("用户名")
        user_name_label.setFont(QFont('Microsoft YaHei', 15))
        user_name_edit = QLineEdit("请输入用户名")
        passwd_label = QLabel("密码")
        passwd_label.setFont(QFont('Microsoft YaHei', 15))
        passwd_edit = QLineEdit("请输入密码")
        passwd_edit.resize(100, 500)
        passwd_edit.setEchoMode(QLineEdit.Password)
        user_passwd_layout.addRow(user_name_label, user_name_edit)
        user_passwd_layout.addRow(passwd_label, passwd_edit)
        # self.setLayout(user_passwd_layout)

        # 标题
        title_layout = QHBoxLayout()
        icon_title = QLabel()
        # icon_title.setGeometry()
        icon_title.setPixmap(QPixmap('./images/数据库.png'))
        title_label = QLabel("数据库检查系统")
        title_label.setFont(QFont('Microsoft YaHei', 25))
        title_layout.addWidget(icon_title)
        title_layout.addWidget(title_label)
        self.setLayout(title_layout)

        # 登录按钮
        login_button = QPushButton("立即登录")
        login_button.resize(500, 500)


        # 全局布局设置
        all_layout = QVBoxLayout()
        title_widget = QWidget()
        user_passwd_widget = QWidget()
        title_widget.setLayout(title_layout)
        user_passwd_widget.setLayout(user_passwd_layout)
        all_layout.addWidget(title_widget)
        all_layout.addWidget(user_passwd_widget)
        all_layout.addWidget(login_button)
        self.setLayout(all_layout)

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
