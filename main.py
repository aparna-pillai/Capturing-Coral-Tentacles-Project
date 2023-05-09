import sys
import platform

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from LoginWindow import *
from CoralWindow import *

class Capturing_Coral_Manager(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        
        if platform.system() == 'Windows':
            desktop = QApplication.desktop()
            screenRect = desktop.screenGeometry()
            self.resize(screenRect.width(), screenRect.height())
            
        self.showMaximized()
    
        self.generalLayout = QGridLayout()

        self.login = Login_Window()
        self.login.submitButtonLogin.clicked.connect(self.moveToNextScreen)
        self.username = ""
        self.main = Coral_Window(self.username)

        self.generalLayout.addWidget(self.login, 0, 0)

        self.centralWidget = QWidget(self)
        self.centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(self.centralWidget)

        # Shortcuts
        self.login_shortcut = QShortcut(Qt.Key_Return, self)
        self.login_shortcut.activated.connect(self.moveToNextScreen)

        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.quit_shortcut.activated.connect(self.close)

    def moveToNextScreen(self):
        if (self.login.check_code_on_initial_login() != None):
            self.username = self.login.check_code_on_initial_login()
            self.generalLayout.removeWidget(self.login)
            self.login.hide()
            self.main = Coral_Window(self.username)
            self.generalLayout.addWidget(self.main, 0, 0)

            self.login_shortcut.activated.disconnect()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Capturing_Coral_Manager()
    gui.show()
    sys.exit(app.exec_())
