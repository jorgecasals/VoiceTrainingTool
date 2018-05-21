import sys
import ViewsNavigator
import Services.ServiceProvider
import Session

from PyQt4 import QtCore, QtGui,uic

class LoginController (QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(LoginController, self).__init__(parent)
        self.user_service = Services.ServiceProvider.user_service
        uic.loadUi('..\UI\login.ui', self)
        self.register_buttons_actions()
        self.load_data()
        self.show()

    def register_buttons_actions(self):
        self.login_btn_ok.clicked.connect(self.click_ok)
        self.login_btn_cancel.clicked.connect(self.click_cancel)
        self.login_btn_register.clicked.connect(self.click_register)

    def load_data(self):
        users = self.user_service.get_all_users_names()
        self.login_cmb_users.clear()
        self.login_cmb_users.addItems(users)

    def click_ok(self):
        Session.user_name = str(self.login_cmb_users.currentText())
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.trainings)

    def click_cancel(self):
        self.close()

    def showEvent(self, *args, **kwargs):
        self.load_data()

    def click_register(self):
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.register)
