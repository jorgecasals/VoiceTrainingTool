# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sun Apr 08 15:56:39 2018
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class login(object):
    def setupUi(self, win_plot):
        win_plot.setObjectName(_fromUtf8("win_plot"))
        win_plot.resize(370, 161)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(win_plot.sizePolicy().hasHeightForWidth())
        win_plot.setSizePolicy(sizePolicy)
        win_plot.setMinimumSize(QtCore.QSize(370, 161))
        win_plot.setMaximumSize(QtCore.QSize(370, 161))
        self.centralwidget = QtGui.QWidget(win_plot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.login_lbl_welcome = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Tahoma"))
        font.setPointSize(11)
        self.login_lbl_welcome.setFont(font)
        self.login_lbl_welcome.setObjectName(_fromUtf8("login_lbl_welcome"))
        self.gridLayout.addWidget(self.login_lbl_welcome, 0, 0, 1, 3)
        self.login_lbl_user = QtGui.QLabel(self.centralwidget)
        self.login_lbl_user.setObjectName(_fromUtf8("login_lbl_user"))
        self.gridLayout.addWidget(self.login_lbl_user, 1, 0, 1, 1)
        self.login_cmb_users = QtGui.QComboBox(self.centralwidget)
        self.login_cmb_users.setObjectName(_fromUtf8("login_cmb_users"))
        self.gridLayout.addWidget(self.login_cmb_users, 1, 1, 1, 2)
        self.login_btn_cancel = QtGui.QPushButton(self.centralwidget)
        self.login_btn_cancel.setObjectName(_fromUtf8("login_btn_cancel"))
        self.gridLayout.addWidget(self.login_btn_cancel, 2, 1, 1, 1)
        self.login_btn_ok = QtGui.QPushButton(self.centralwidget)
        self.login_btn_ok.setObjectName(_fromUtf8("login_btn_ok"))
        self.gridLayout.addWidget(self.login_btn_ok, 2, 2, 1, 1)
        win_plot.setCentralWidget(self.centralwidget)

        self.retranslateUi(win_plot)
        QtCore.QMetaObject.connectSlotsByName(win_plot)

    def retranslateUi(self, win_plot):
        win_plot.setWindowTitle(_translate("win_plot", "Login", None))
        self.login_lbl_welcome.setText(_translate("win_plot", "Welcome to Voice Trainer!", None))
        self.login_lbl_user.setText(_translate("win_plot", "User", None))
        self.login_btn_cancel.setText(_translate("win_plot", "Cancel", None))
        self.login_btn_ok.setText(_translate("win_plot", "OK", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    win_plot = QtGui.QMainWindow()
    ui = login()
    ui.setupUi(win_plot)
    win_plot.show()
    sys.exit(app.exec_())

