# Source for image upload PyQt code:
# https://stackoverflow.com/questions/60614561/how-to-ask-user-to-input-an-image-in-pyqt5
# Source for counting dots
# https://stackoverflow.com/questions/60603243/detect-small-dots-in-image 

import sys
from tkinter import mainloop
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from tkinter import *
from ImageTrial import ImageTrial

import cv2 as cv
import os
import numpy as np
from numpy import asarray

from LoginWindow import Login_Window
from CoralWindow import Coral_Window


COUNT = 0
PATH = ""

class Capturing_Coral_Manager(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        self.showMaximized()
        self.generalLayout = QGridLayout()

        self.login = Login_Window()
        self.login.submitButtonLogin.clicked.connect(self.moveToNextScreen)
        self.main = Coral_Window()

        self.generalLayout.addWidget(self.login, 0, 0)

        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

    def moveToNextScreen(self):
        print("Clicked submit")
        self.generalLayout.removeWidget(self.login)
        self.login.hide()
        self.generalLayout.addWidget(self.main, 0, 0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Capturing_Coral_Manager()
    gui.show()
    sys.exit(app.exec_())
