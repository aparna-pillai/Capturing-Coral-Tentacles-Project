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

def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    widget.place(x=x,y=y)


class Image(QWidget):

    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        self.fileName = ""
        btn = QPushButton('Browse')
        self.pix = QPixmap()
        btn.clicked.connect(self.open_image)
        
        
        grid = QGridLayout(self)
        #basewidth = 100
        #img = Image.open(self.photo)
        grid.addWidget(btn, 0, 0, Qt.AlignTop)
        grid.addWidget(self.photo, 1, 0)
        self.setAcceptDrops(True)

    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            photo_path = str(filename)
            print(photo_path)
        self.fileName = filename  
        self.pix = QPixmap(filename)
    
        
        self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.FastTransformation))
       
        global PATH
        PATH = str(photo_path)

    def addMarker(self):
        self.painterInstance = QPainter(self.pix)

            # set rectangle color and thickness
        self.penRectangle = QPen(Qt.red)
        self.penRectangle.setWidth(3)

            # draw rectangle on painter
        self.painterInstance.setPen(self.penRectangle)
        self.painterInstance.drawRect(0,0,20,20)
        
        self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.FastTransformation))

        self.painterInstance.bind("<Button-1>",drag_start)
        self.painterInstance.bind("<B1-Motion>",drag_motion)

        self.painterInstance.bind("<Button-1>",drag_start)
        self.painterInstance.bind("<B1-Motion>",drag_motion)
        
    def get_filename(self):
        return self.fileName