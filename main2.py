# Source for image upload PyQt code:
# https://stackoverflow.com/questions/60614561/how-to-ask-user-to-input-an-image-in-pyqt5
# Source for counting dots
# https://stackoverflow.com/questions/60603243/detect-small-dots-in-image 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2 as cv
import numpy as np

COUNT = 0
PATH = ""

from Image import Image

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "Main")
        tabs.addTab(self.networkTabUI(), "Gallery")
        layout.addWidget(tabs)

    def generalTabUI(self):
        #"""Create the General page UI."""
        generalTab = QWidget()
        #layout = QVBoxLayout()
        #layout.addWidget(QCheckBox("General Option 1"))
        #layout.addWidget(QCheckBox("General Option 2"))
        #generalTab.setLayout(layout)
    
        self.generalLayout = QGridLayout()

        #centralWidget = QWidget(self)
        #centralWidget.setLayout(self.generalLayout)
        #self.setCentralWidget(centralWidget)
        
        self.photo = Image()
        self.generalLayout.addWidget(self.photo, 0, 0)

        self.galleryButton = QPushButton("Gallery: Saved Pictures && Counts")
        self.savePicButton = QPushButton("Save Picture")
        
        self.countButton = QPushButton("Count")
        #self.countButton.clicked.connect(self.countTentacles)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(COUNT))
        self.fullExtLabel = QLabel("Fully Extended:")
        self.fullExtDisplay = QLineEdit("0")
        self.partExtLabel = QLabel("Partially Extended:")
        self.partExtDisplay = QLineEdit("0")

        self.addFullMarkerButton = QPushButton("Add 1 Fully Extended Marker")
        self.addPartMarkerButton = QPushButton("Add 1 Partially Extended Marker")
        self.removeMarkerButton = QPushButton("Remove Selected Marker")

        self.galleryButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: blue;"
            "border-left-color: blue;"
            "border-right-color: blue;"
            "border-bottom-color: blue;"
            "color: blue;"
        )

        self.savePicButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: green;"
            "border-left-color: green;"
            "border-right-color: green;"
            "border-bottom-color: green;"
            "color: green;"
        )

        self.countButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: red;"
            "border-left-color: red;"
            "border-right-color: red;"
            "border-bottom-color: red;"
            "color: red;"
        )

        self.setStyleSheet(
            "QLabel {color: purple;}"
        )


        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
        self.smallerGridLayout.addWidget(self.countDisplay, 0, 1)
        self.smallerGridLayout.addWidget(self.fullExtLabel, 1, 0)
        self.smallerGridLayout.addWidget(self.fullExtDisplay, 1, 1)
        self.smallerGridLayout.addWidget(self.partExtLabel, 2, 0)
        self.smallerGridLayout.addWidget(self.partExtDisplay, 2, 1)
        
        self.smallGridLayout = QGridLayout()
        #self.smallGridLayout.addWidget(self.galleryButton, 0, 0)
        self.smallGridLayout.addWidget(self.savePicButton, 1, 0)
        self.smallGridLayout.addWidget(self.countButton, 2, 0)
        self.smallGridLayout.addLayout(self.smallerGridLayout, 3, 0)
        self.smallGridLayout.addWidget(self.addFullMarkerButton, 4, 0)
        self.smallGridLayout.addWidget(self.addPartMarkerButton, 5, 0)
        self.smallGridLayout.addWidget(self.removeMarkerButton, 6, 0)

        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        generalTab.setLayout(self.generalLayout)
        return generalTab
    
    def networkTabUI(self):
        """Create the Network page UI."""
        networkTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Network Option 1"))
        layout.addWidget(QCheckBox("Network Option 2"))
        networkTab.setLayout(layout)
        return networkTab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())