import sys
import platform
import typing
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from LoginWindow import *
from CoralWindow import *
from connectToDatabase import *

from splash_screen import Ui_SplashScreen

counter = 0

class Capturing_Coral_Manager(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        
        self.resize(380, 500)

        self.generalLayout = QGridLayout()

        palette = self.palette()
        palette.setBrush(QPalette.Window, QColor(66, 22, 161))  
        self.setPalette(palette)

        self.login = Login_Window()

        self.login.pushButton.clicked.connect(self.moveToNextScreen)
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

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(35)

        self.show()

    def progress(self):
        global counter
        self.ui.progressBar.setValue(counter)

        if counter > 100:
            self.timer.stop()
            self.main = Capturing_Coral_Manager()
            self.main.show()

            self.close()

        counter += 1



if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # gui = Capturing_Coral_Manager()
    # gui.show()
    # sys.exit(app.exec_())

    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
