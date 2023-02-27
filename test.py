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
#from PIL import Image
from datetime import date

from Image2 import *
from RecordInfoWindow import *

from coral_count import count_tentacles_actual, get_count

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        #self.setGeometry(0, 0, 1000, 800)
        self.showMaximized()
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 10
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "Main")
        tabs.addTab(self.recordTabUI(), "Record")
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
        
        self.savePicButton = QPushButton("Save Picture to Record")
        self.savePicButton.clicked.connect(self.recordInfo)
        
        self.countButton = QPushButton("Count")
        self.countButton.clicked.connect(self.countTentacles)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(0))

        self.addFullMarkerButton = QPushButton("Add Marker")
        self.addFullMarkerButton.clicked.connect(self.addFullMarker)

        
        self.countLabel.setStyleSheet(
            "color: #112d4e;"
        )
                
        self.savePicButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )

        self.countButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        
        self.addFullMarkerButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )

        self.setStyleSheet(
            "QLabel {color: purple;}"
        )
        
        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
        self.smallerGridLayout.addWidget(self.countDisplay, 0, 1)
        
        self.smallGridLayout = QGridLayout()
        #self.smallGridLayout.addWidget(self.galleryButton, 0, 0)
        self.smallGridLayout.addWidget(self.savePicButton, 1, 0)
        self.smallGridLayout.addWidget(self.countButton, 2, 0)
        self.smallGridLayout.addLayout(self.smallerGridLayout, 3, 0)
        self.smallGridLayout.addWidget(self.addFullMarkerButton, 4, 0)

        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        generalTab.setLayout(self.generalLayout)
        return generalTab
    
    def recordTabUI(self):
        """Create the Network page UI."""
        recordTab = QWidget()
        layout = QGridLayout()

        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["FILENAME", "TENTACLE COUNT", "NAME OF PERSON", "DATE UPLOADED", "NOTES"]) 
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.tableWidget.setObjectName("tableWidget")
        # scroll bar
        scroll_bar = QScrollBar(self)
 
        # setting style sheet to the scroll bar
        scroll_bar.setStyleSheet("QScrollBar"
                             "{"
                             "background : #e1eedd;"
                             "}"
                             "QScrollBar::handle"
                             "{"
                             "background : #dbe2ef;"
                             "}"
                             "QScrollBar::handle::pressed"
                             "{"
                             "background : #00adb5;"
                             "}"
        )
 
        # setting vertical scroll bar to it
        self.tableWidget.setVerticalScrollBar(scroll_bar)
 
 
        layout.addWidget(self.tableWidget, 0, 0) 
        
        
        self.tableWidget.setStyleSheet(
            "border: 1px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )

        header.setStyleSheet(
            "color: #112d4e;"
        )
                
        self.btnLoad = QPushButton("Load")
        load_dotenv('config.env')
        self.btnLoad.clicked.connect(self.DBConnect)
        self.btnDelete = QPushButton("Delete")
        load_dotenv('config.env')
        self.btnDelete.clicked.connect(self.deleteRow)
        
        self.btnLoad.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        self.btnDelete.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        
        self.smGridLayout = QGridLayout()
        #self.smallGridLayout.addWidget(self.galleryButton, 0, 0)
        self.smGridLayout.addWidget(self.btnLoad, 0, 0)
        self.smGridLayout.addWidget(self.btnDelete, 0, 1)

        layout.addLayout(self.smGridLayout, 1, 0)
        
        
        
        #layout.addWidget(QCheckBox("Network Option 2"))
        recordTab.setLayout(layout)
        
        return recordTab
    
        
    def deleteRow(self):
        print("Hi")
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            filenameForQuery = item[0].text()
            print (item[0].text())
     
            try:
                mydb = mc.connect(
                    host=os.environ.get('HOST'),
                    user=os.environ.get('USERNAME'),
                    password=os.getenv('PASSWORD'), 
                    database=os.getenv('DATABASE')             
                )
                mycursor = mydb.cursor()
                #DELETE FROM image_info WHERE filename=item[0].text()
                
                sql_delete = "DELETE FROM image_info WHERE filename = %s"
                sql_data = (filenameForQuery,)

                mycursor.execute(sql_delete, sql_data)
            
                #mycursor.execute("DELETE FROM image_info WHERE filename = ?)", (item[0].text(),))
                
                mydb.commit()

                #QMessageBox.about(self, "Connection", "Database Connected Successfully")
                print(mydb)
                
                mydb.close()
            except mydb.Error as e:
                print("Failed To Connect to Database")
            self.tableWidget.removeRow(currentRow)
    
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
            
    def recordInfo(self, checked):
        if self.photo.get_filename() == "":
            QMessageBox.about(self, "Warning", "You did not upload an image!")
        #if self.g is None:
        else:
            self.g = RecordInfoWindow()
            self.g.submitButton.clicked.connect(self.gatheringInfo)
            self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
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
                mycursor.execute("INSERT INTO image_info VALUES (%s, %s, %s, %s, %s)", (self.photo.get_filename(), self.photo.marker_count+self.count, self.g.get_name(),  date.today(), self.g.get_notes()))
                mydb.commit()

                #QMessageBox.about(self, "Connection", "Database Connected Successfully")
        
                
                print(mydb)
                self.g.close()
                mydb.close()
                
            except mydb.Error as e:
                print("Failed To Connect to Database")

    def countTentacles(self):
        # Get labeled image and set path of the Image2 to new path
        labeled_image_path = count_tentacles_actual(self.photo.path)
        self.photo.path = labeled_image_path

        # Resize and add image to pixmap for display
        self.photo.pix = QPixmap(labeled_image_path)
        self.photo.smaller_pixmap = self.photo.pix.scaled(self.photo.view.width(), self.photo.view.height())
        self.photo.scene.clear()
        self.photo.scene.addPixmap(self.photo.smaller_pixmap)

        # Get tentacle count
        self.countDisplay.setText(str(get_count()))

        # Delete the new resized.jpg created in the main folder (for some reason)
        if (os.path.exists('resized.jpg')):
            os.remove('resized.jpg')
    
    def addFullMarker(self):
        self.photo.add_marker()
        self.countDisplay.setText("{0}".format(self.photo.marker_count+self.count))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())