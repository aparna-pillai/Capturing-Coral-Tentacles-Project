import sys

from PhotoLabel import PhotoLabel

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2 as cv
import numpy as np

COUNT = 0
PATH = ""

class Image(QWidget):

    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        btn = QPushButton('Browse')
        btn.clicked.connect(self.open_image)
        
        grid = QGridLayout(self)
        grid.addWidget(btn, 0, 0, Qt.AlignTop)
        grid.addWidget(self.photo, 1, 0)
        self.setAcceptDrops(True)
        self.resize(300, 200)

    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            photo_path = str(filename)
            
            self.photo.setPixmap(QPixmap(filename))
        
        global PATH
        PATH = str(photo_path)