import sys

from PhotoLabel import PhotoLabel

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
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
        marker_btn = QPushButton('Add Marker')

        self.pix = QPixmap()
        btn.clicked.connect(self.open_image)
        marker_btn.clicked.connect(self.add_marker)
        
        self.path = ""
        self.file = ""
        
        grid = QGridLayout(self)
        #basewidth = 100
        #img = Image.open(self.photo)
        grid.addWidget(btn, 0, 0, Qt.AlignTop)
        
        grid.addWidget(self.photo, 1, 0)
        grid.addWidget(marker_btn, 0, 1, Qt.AlignTop)

        self.marker_counter = QLabel("Marker Count: 0")
        grid.addWidget(self.marker_counter, 0, 3, Qt.AlignTop)
        
        btn_print = QPushButton('Print Marker Coordinates')
        btn_print.clicked.connect(self.print_markers)
        grid.addWidget(btn_print, 0, 4, Qt.AlignTop)

        # btn_print = QPushButton('Print Circles')
        # btn_print.clicked.connect(self.print_circles)
        # grid.addWidget(btn_print, 0, 2, Qt.AlignTop)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        grid.addWidget(self.view, 1, 0, 1, 4)
        
        self.marker_count = 0
        self.markers = []

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
        self.scene.clear()
        self.scene.addPixmap(self.pix)
        #self.setGeometry(0, 0, self.pix.width(), self.pix.height())

        self.photo.setPixmap(self.pix.scaledToHeight(700, Qt.FastTransformation))
       
        #self.path = str(photo_path)
        
    def add_marker(self):
        ellipse = QGraphicsEllipseItem(0, 0, 15, 15)
        ellipse.setBrush(QBrush(Qt.yellow))
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(ellipse)
        self.marker_count += 1
        self.marker_counter.setText("Marker Count: {}".format(self.marker_count))
        self.markers.append(ellipse)
    
    def print_markers(self):
        for marker in self.markers:
            print("({}, {}).".format(marker.x(), marker.y()))  

    # def addMarker(self):
    #     self.painterInstance = QPainter(self.pix)

    #     # set rectangle color and thickness
    #     self.penRectangle = QPen(Qt.red)
    #     self.penRectangle.setWidth(3)

    #     #     # draw rectangle on painter
    #     self.painterInstance.setPen(self.penRectangle)
    #     self.painterInstance.drawRect(0,0,20,20)
        
    #     self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.FastTransformation))

    #     def drag_start(event):
    #         widget = event.widget
    #         widget.startX = event.x
    #         widget.startY = event.y

    #     def drag_motion(event):
    #         widget = event.widget
    #         x = widget.winfo_x() - widget.startX + event.x
    #         y = widget.winfo_y() - widget.startY + event.y
    #         widget.place(x=x,y=y)

    #     self.painterInstance.bind("<Button-1>",drag_start)
    #     self.painterInstance.bind("<B1-Motion>",drag_motion)
        
    # def get_filename(self):
    #     return self.fileName
