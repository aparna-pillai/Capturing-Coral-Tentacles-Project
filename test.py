# Source for image upload PyQt code:
# https://stackoverflow.com/questions/60614561/how-to-ask-user-to-input-an-image-in-pyqt5
# Source for counting dots
# https://stackoverflow.com/questions/60603243/detect-small-dots-in-image 

import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import cv2 as cv
import numpy as np
import mysql.connector as mc
import os
from dotenv import load_dotenv

COUNT = 0
PATH = ""
IMAGE_ID = 0

from Image import Image
#from GalleryInfoWindow import GalleryInfoWindow

class GalleryInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        #self.label = QLabel("Another Window")
        
        self.image_id_Label = QLabel("Image ID:")
        self.image_id_Display = QLineEdit("{0}".format(IMAGE_ID))
        
        self.filename_Label = QLabel("Filename:")
        self.filename_Display = QLineEdit("{0}".format(PATH))
        
        self.tentacle_count_Label = QLabel("Tentacle Count:")
        self.tentacle_count_Display = QLineEdit("{0}".format(COUNT))
        
        self.name_of_person_Label = QLabel("Name:")
        self.name_of_person_Display = QLineEdit()
        
        #self.smallerGridLayout = QGridLayout()
        layout.addWidget(self.image_id_Label, 0, 0)
        layout.addWidget(self.image_id_Display, 0, 1)
        layout.addWidget(self.filename_Label, 1, 0)
        layout.addWidget(self.filename_Display, 1, 1)
        layout.addWidget(self.tentacle_count_Label, 2, 0)
        layout.addWidget(self.tentacle_count_Display, 2, 1)
        layout.addWidget(self.name_of_person_Label, 3, 0)
        layout.addWidget(self.name_of_person_Display, 3, 1)
        
        print(self.name_of_person_Display.text())
        
        
        #layout.addWidget(self.label)
        self.setLayout(layout)
        
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        self.setGeometry(0, 0, 1000, 800)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "Main")
        tabs.addTab(self.galleryTabUI(), "Gallery")
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

        self.g = None
        
        self.savePicButton = QPushButton("Save Picture to Gallery")
        self.savePicButton.clicked.connect(self.galleryInfo)
        
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
    
    def galleryTabUI(self):
        """Create the Network page UI."""
        galleryTab = QWidget()
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["IMAGE_ID", "FILENAME", "TENTACLE COUNT", "NAME OF PERSON", "DATE UPLOADED"])
        self.tableWidget.setObjectName("tableWidget")
        layout.addWidget(self.tableWidget) 
        
        self.btn = QPushButton("Load")
        load_dotenv('config.env')
        self.btn.clicked.connect(self.DBConnect)
        
        layout.addWidget(self.btn)
        
        #layout.addWidget(QCheckBox("Network Option 2"))
        galleryTab.setLayout(layout)
        
        return galleryTab
    
        
    def DBConnect(self):
         
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.environ.get('USERNAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM image_info")

            result = mycursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                print(row_number)
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    #print(column_number)
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))


            #QMessageBox.about(self, "Connection", "Database Connected Successfully")
            print(mydb)
         #connection.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
            
    def galleryInfo(self, checked):
        if self.g is None:
            self.g = GalleryInfoWindow()
            self.g.setGeometry(self.frameGeometry().width(), 0, 300, 300)
            self.g.show()
        else:
            self.g.close()
            self.g = None
            
        
    def countTentacles(self):
        print(COUNT)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())