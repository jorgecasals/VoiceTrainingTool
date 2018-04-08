import sys
import ViewsNavigator

from PyQt4 import QtCore, QtGui,uic
import Services.ServiceProvider

class RegisterController (QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RegisterController, self).__init__(parent)
        uic.loadUi('..\UI\\register.ui', self)
        self.user_service = Services.ServiceProvider.user_service
        self.register_buttons_actions()
        self.show()

    def register_buttons_actions(self):
        self.register_btn_create.clicked.connect(self.click_create)
        self.register_btn_cancel.clicked.connect(self.click_cancel)

    def click_create(self):
        user_name = str(self.register_tb_name.text())
        if not user_name.isspace():
            self.user_service.create_user(user_name)
            self.go_to_login()


    def click_cancel(self):
        self.go_to_login()

    def go_to_login(self):
        ViewsNavigator.navigator.navigate_to_view(self, ViewsNavigator.navigator.login)


