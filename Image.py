import sys

from PhotoLabel import PhotoLabel

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from tkinter import *

from PIL import Image, ImageTk

import cv2 as cv
import numpy as np

#photo_path = ""

class Image(QWidget):
    
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        
        btn = QPushButton('Browse')
        self.pix = QPixmap()
        btn.clicked.connect(self.open_image)
        
        self.path = ""
        self.file = ""
        
        grid = QGridLayout(self)
        #basewidth = 100
        #img = Image.open(self.photo)
        grid.addWidget(btn, 0, 0, Qt.AlignTop)
        grid.addWidget(self.photo, 1, 0)
        self.setAcceptDrops(True)
        
    def open_image(self, filename=None):
        #global photo_path
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            self.path = str(filename)
            url = QUrl.fromLocalFile(filename)
            self.file = QFileInfo(filename).fileName()
            #path = str(filename)
            #print("Hello: " + self.path)
        
        self.pix = QPixmap(filename)
    
        
        self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.FastTransformation))
       
        #self.path = str(photo_path)
        
    def get_filename(self):
        return self.file
        
    def addMarker(self):
        self.painterInstance = QPainter(self.pix)

            # set rectangle color and thickness
        self.penRectangle = QPen(Qt.red)
        self.penRectangle.setWidth(3)

            # draw rectangle on painter
        self.painterInstance.setPen(self.penRectangle)
        self.painterInstance.drawRect(0,0,20,20)
        
        self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.FastTransformation))

        