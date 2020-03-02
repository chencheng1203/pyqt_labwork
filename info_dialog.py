# -*- encoding:utf-8 -*-
# @Time: 2020/2/25 18:26

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QPushButton, QLineEdit, QDesktopWidget, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QPixmap, QPalette, QIcon, QFont


class info_not_fill(QWidget):
    def __init__(self):
        super(info_not_fill, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('提示')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"./images/软件图标.ico"))
        self.resize(200, 100)
        self.center()
        self.setFixedSize(self.width(), self.height())

        all_layout = QVBoxLayout()
        message_label_layout = QHBoxLayout()
        message_label = QLabel('请继续完善信息')
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


class user_already_exist(QWidget):
    def __init__(self):
        super(user_already_exist, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('提示')   # 设置窗口名称
        self.setWindowIcon(QIcon(r"./images/软件图标.ico"))
        self.resize(200, 100)
        self.center()
        self.setFixedSize(self.width(), self.height())

        all_layout = QVBoxLayout()
        message_label_layout = QHBoxLayout()
        message_label = QLabel('用户名存在')
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