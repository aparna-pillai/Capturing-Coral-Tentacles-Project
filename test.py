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
from PIL import Image
from datetime import date

from Image2 import *
from GalleryInfoWindow import *
class Window(QWidget):

    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        self.setGeometry(0, 0, 1000, 800)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 10
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
        
        self.photo = Image2()

        self.generalLayout.addWidget(self.photo, 0, 0)

        self.g = None
        
        self.savePicButton = QPushButton("Save Picture to Gallery")
        self.savePicButton.clicked.connect(self.galleryInfo)
        
        self.countButton = QPushButton("Count")
        #self.countButton.clicked.connect(self.countTentacles)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format("0"))
        self.fullExtLabel = QLabel("Fully Extended:")
        self.fullExtDisplay = QLineEdit("0")
        self.partExtLabel = QLabel("Partially Extended:")
        self.partExtDisplay = QLineEdit("0")

        self.addFullMarkerButton = QPushButton("Add 1 Fully Extended Marker")
        self.addFullMarkerButton.clicked.connect(self.addFullMarker)
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
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["FILENAME", "TENTACLE COUNT", "NAME OF PERSON", "DATE UPLOADED"])
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
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
            
    def galleryInfo(self, checked):
        #if self.g is None:
            self.g = GalleryInfoWindow()
            self.g.submitButton.clicked.connect(self.gatheringInfo)
            self.g.setGeometry(self.frameGeometry().width(), 0, 300, 300)
            self.g.show()
        #else:
            
          #  self.g.close()
          #  self.g = None
            
    def gatheringInfo(self):        
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.environ.get('USERNAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
                        

            #mySql_insert_query = """INSERT INTO image_info(image_id, filename, tentacle_count, name_of_person, date_uploaded) 
              #      VALUES (?, ?, ?, ?, ?)""", (self.g.get_id(), self.photo.get_filename(), self.count, self.g.get_name(),  date.today())
            
            

                                                  
            #"""INSERT INTO image_info
             #                       VALUES (2, "Hi", 2, "Aditi", DATE '2015-12-17') """
            
    
            mycursor = mydb.cursor()
            
            #mycursor.execute(mySql_insert_query)
            
            mycursor.execute("INSERT INTO image_info VALUES (%s, %s, %s, %s)", (self.photo.get_filename(), self.count, self.g.get_name(),  date.today()))
            
            mydb.commit()

            #QMessageBox.about(self, "Connection", "Database Connected Successfully")
            print(mydb)
            self.g.close()
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
           
        
    # def countTentacles(self):
    #     print("YAAAS: " + self.photo.get_filename())
    #     print(self.g.get_id())
    #     print(self.count)
    #     print(self.g.get_name())
    #     print(date.today())
    #     #print(COUNT)
    #     #print(GalleryInfoWindow.id)
    #     #print(self.photo.get_filename)
    
    def addFullMarker(self):
        self.photo.addMarker()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())