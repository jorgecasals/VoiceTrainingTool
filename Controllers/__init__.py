import sys
import ViewsNavigator
from PyQt4 import QtCore, QtGui,uic

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ViewsNavigator.navigator.navigate_to_view(None, ViewsNavigator.navigator.login)
    sys.exit(app.exec_())