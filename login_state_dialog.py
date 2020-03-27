# -*- encoding:utf-8 -*-
# @Time: 2020/1/12 9:35

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QDesktopWidget, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont


class sucess_login(QWidget):
    def __init__(self):
        super(sucess_login, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录成功')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"D:\Code\PyQt\bupt_prj01\images/软件图标.ico"))
        self.resize(200, 100)
        self.center()
        self.setFixedSize(self.width(), self.height())

        all_layout = QVBoxLayout()
        message_label_layout = QHBoxLayout()
        message_label = QLabel('登录成功')
        message_label_w1 = QWidget()
        self.message_label_btn = QPushButton("确定")
        self.message_label_btn.clicked.connect(self.close)

        message_label_layout.addStretch(1)
        message_label_layout.addWidget(message_label)
        message_label_layout.addStretch(1)
        message_label_w1.setLayout(message_label_layout)

        all_layout.addWidget(message_label_w1)
        all_layout.addWidget(self.message_label_btn)
        self.setLayout(all_layout)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class failed_login_not_input(QWidget):
    def __init__(self):
        super(failed_login_not_input, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录成功')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"D:\Code\PyQt\bupt_prj01\images/软件图标.ico"))
        self.resize(200, 100)
        self.center()
        self.setFixedSize(self.width(), self.height())

        all_layout = QVBoxLayout()
        message_label_layout = QHBoxLayout()
        message_label = QLabel('请输入用户名和密码')
        message_label_w1 = QWidget()
        self.message_label_btn = QPushButton("确定")
        self.message_label_btn.clicked.connect(self.close)

        message_label_layout.addStretch(1)
        message_label_layout.addWidget(message_label)
        message_label_layout.addStretch(1)
        message_label_w1.setLayout(message_label_layout)

        all_layout.addWidget(message_label_w1)
        all_layout.addWidget(self.message_label_btn)
        self.setLayout(all_layout)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class failed_login_passwd_error(QWidget):
    def __init__(self):
        super(failed_login_passwd_error, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('登录成功')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"D:\Code\PyQt\bupt_prj01\images/软件图标.ico"))
        self.resize(200, 100)
        self.center()
        self.setFixedSize(self.width(), self.height())

        all_layout = QVBoxLayout()
        message_label_layout = QHBoxLayout()
        message_label = QLabel('用户名或密码不正确')
        message_label_w1 = QWidget()
        self.message_label_btn = QPushButton("确定")
        self.message_label_btn.clicked.connect(self.close)

        message_label_layout.addStretch(1)
        message_label_layout.addWidget(message_label)
        message_label_layout.addStretch(1)
        message_label_w1.setLayout(message_label_layout)

        all_layout.addWidget(message_label_w1)
        all_layout.addWidget(self.message_label_btn)
        self.setLayout(all_layout)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_win = failed_login_not_input()
    login_win.show()
    sys.exit(app.exec())