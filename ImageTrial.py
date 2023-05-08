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

class ImageTrial(QWidget):
    
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        
        btn = QPushButton('Browse')
        marker_btn = QPushButton('Add Marker')
        remove_marker_btn = QPushButton('Remove Marker')

        self.pix = QPixmap()
        btn.clicked.connect(self.open_image)
        marker_btn.clicked.connect(self.add_marker)
        remove_marker_btn.clicked.connect(self.remove_marker)

        
        self.path = ""
        self.file = ""
        
        grid = QGridLayout(self)

        grid.addWidget(btn, 0, 0, Qt.AlignTop)
        
        grid.addWidget(self.photo, 1, 0)
        grid.addWidget(marker_btn, 0, 1, Qt.AlignTop)
        grid.addWidget(remove_marker_btn, 0, 2, Qt.AlignTop)


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
        grid.addWidget(self.view, 1, 0, 1, 5)
        
        self.marker_count = 0
        self.markers = []
        self.list = []

        self.setAcceptDrops(True)

        self.selected_marker = None
        
    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            self.path = str(filename)
            url = QUrl.fromLocalFile(filename)
            self.file = QFileInfo(filename).fileName()
        
        self.pix = QPixmap(filename)
        self.scene.clear()
        self.scene.addPixmap(self.pix)
        #self.setGeometry(0, 0, self.pix.width(), self.pix.height())

        self.photo.setPixmap(self.pix.scaledToHeight(625, Qt.FastTransformation))
       
        
    def add_marker(self):
        ellipse = QGraphicsEllipseItem(0, 0, 15, 15)
        ellipse.setBrush(QBrush(Qt.yellow))

        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        ellipse.setFlag(QGraphicsItem.ItemIsSelectable)

        self.scene.addItem(ellipse)
        self.marker_count += 1
        self.marker_counter.setText("Marker Count: {}".format(self.marker_count))
        self.markers.append(ellipse)

    def set_selected_marker(self, marker):
        self.selected_marker = marker  
    
    def remove_marker(self):
        for i, marker in enumerate(self.markers):
            if marker.isSelected():
                self.scene.removeItem(marker)
                self.markers.pop(i)
                self.marker_count -= 1
                self.marker_counter.setText("Marker Count: {}".format(self.marker_count))
                return

    
    def print_markers(self):
        for marker in self.markers:
            self.list.append("({}, {})".format(marker.x(), marker.y()))
        print(self.list) 
