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
from PIL import Image as ImagePIL
from datetime import date
import matplotlib.pyplot as plt

from Image2 import *
from RecordInfoWindow import *

from coral_count import count_tentacles_actual, get_count, get_coordinates

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        #self.setGeometry(0, 0, 1000, 800)
        self.showMaximized()
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 0
        self.list = []
        # Create the tab widget with two tabs
        self.tabs = QTabWidget()
        general_tab = self.generalTabUI()
        record_tab = self.recordTabUI()

        self.tabs.addTab(general_tab, "Main")
        self.tabs.addTab(record_tab, "Record")
        layout.addWidget(self.tabs)

        # Keyboard shortcuts
        self.count_shortcut = QShortcut(Qt.Key_C, self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.load_shortcut = QShortcut(Qt.Key_Return, self)
        self.delete_shortcut = QShortcut(Qt.Key_Delete, self)
        self.tab_shortcut = QShortcut(Qt.Key_Tab, self)
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        
        self.count_shortcut.activated.connect(self.countTentacles)
        self.save_shortcut.activated.connect(self.recordInfo)
        self.load_shortcut.activated.connect(self.DBConnect)
        self.delete_shortcut.activated.connect(self.deleteRow)
        self.tab_shortcut.activated.connect(self.switchTabs)
        self.quit_shortcut.activated.connect(self.close)
        
    def switchTabs(self):
        if self.tabs.isTabEnabled(0):
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(0, False)
        else:
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, False)

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
        
        self.instructionsButton = QPushButton("Instructions")
        self.instructionsButton.clicked.connect(self.instruct)
        
        self.savePicButton = QPushButton("Save Picture to Record")
        self.savePicButton.clicked.connect(self.recordInfo)
        
        self.countButton = QPushButton("Count")
        self.countButton.clicked.connect(self.countTentacles)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(0))
        
        self.removeMarkerButton = QPushButton("Remove Marker")
        self.removeMarkerButton.clicked.connect(self.removeMarker)

        self.setMouseTracking(True)

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
        self.smallerGridLayout.addWidget(self.countDisplay, 0, 1)
        
        self.smallGridLayout = QGridLayout()
        self.smallGridLayout.addWidget(self.instructionsButton, 0, 0)
        self.smallGridLayout.addWidget(self.savePicButton, 1, 0)
        self.smallGridLayout.addWidget(self.countButton, 2, 0)
        self.smallGridLayout.addLayout(self.smallerGridLayout, 3, 0)
        self.smallGridLayout.addWidget(self.removeMarkerButton, 4, 0)

        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        
        # Stylesheets
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
        
        self.removeMarkerButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        
        self.instructionsButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
            "background-color : #00adb5;"
        )

        self.setStyleSheet(
            "QLabel {color: purple;}"
        )

        generalTab.setLayout(self.generalLayout)
        return generalTab
    
    def instruct(self):
        QMessageBox.about(self, "Information", "Instructions: \nUpload photo and click count button to get the number of tentacles on the coral. \nAfter adding/removing markers, save the picture to the record!")
        
    def recordTabUI(self):
        """Create the Network page UI."""
        recordTab = QWidget()
        layout = QGridLayout()

        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["FILENAME", "TENTACLE COUNT", "NAME OF PERSON", "DATE UPLOADED", "COORDINATES OF MARKERS", "NOTES"]) 
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tableWidget.setObjectName("tableWidget")
        # scroll bar
        scroll_bar = QScrollBar(self)
 
        # setting style sheet to the scroll bar
        scroll_bar.setStyleSheet(
            '''QScrollBar
            {
                background : #e1eedd;
            }
            QScrollBar::handle
            {
                background : #dbe2ef;
            }
            QScrollBar::handle::pressed
            {
                background : #00adb5;
            }'''
        )
 
        # setting vertical scroll bar to it
        self.tableWidget.setVerticalScrollBar(scroll_bar)
 
        layout.addWidget(self.tableWidget, 0, 0) 

        self.btnLoad = QPushButton("Load")
        load_dotenv('config.env')
        self.btnLoad.clicked.connect(self.DBConnect)
        self.btnDelete = QPushButton("Delete")
        load_dotenv('config.env')
        self.btnDelete.clicked.connect(self.deleteRow)

        self.smGridLayout = QGridLayout()
        #self.smallGridLayout.addWidget(self.galleryButton, 0, 0)
        self.smGridLayout.addWidget(self.btnLoad, 0, 0)
        self.smGridLayout.addWidget(self.btnDelete, 0, 1)

        layout.addLayout(self.smGridLayout, 1, 0)

        
        # Stylesheets
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
        
        
        #layout.addWidget(QCheckBox("Network Option 2"))
        recordTab.setLayout(layout)
        
        return recordTab
    

    def deleteRow(self):
        # print("Hi")
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:
                filenameForQuery = item[0].text()
                print (item[0].text())
        
                try:
                    mydb = mc.connect(
                        host=os.environ.get('HOST'),
                        user = os.getenv('NAME'),
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
                user=os.getenv('NAME'),
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
            
    def recordInfo(self):   # checked parameter? Is it needed?
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
                    user=os.getenv('NAME'),
                    password=os.getenv('PASSWORD'), 
                    database=os.getenv('DATABASE')             
                )
                            

                #mySql_insert_query = """INSERT INTO image_info(image_id, filename, tentacle_count, name_of_person, date_uploaded) 
                #      VALUES (?, ?, ?, ?, ?)""", (self.g.get_id(), self.photo.get_filename(), self.count, self.g.get_name(),  date.today())
                
                

                                                    
                #"""INSERT INTO image_info
                #                       VALUES (2, "Hi", 2, "Aditi", DATE '2015-12-17') """
                
        
                mycursor = mydb.cursor()
                
                coordString = ''.join(self.list)
                
                #mycursor.execute(mySql_insert_query)
                mycursor.execute(
                    "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s)", 
                    (
                        self.photo.get_filename(), self.photo.marker_count, 
                        self.g.get_name(), date.today(), coordString, self.g.get_notes()
                    )
                )
                
                self.tableWidget.resizeRowsToContents()
                mydb.commit()

                #QMessageBox.about(self, "Connection", "Database Connected Successfully")
        
                
                print(mydb)
                self.g.close()
                mydb.close()
                
            except mydb.Error as e:
                print("Failed To Connect to Database")

    def countTentacles(self):
        if (self.photo.get_filename() == ""):
            QMessageBox.about(self, "Warning", "Please upload an image.")
        else:
            # Run the model on the currently displayed photo (in Image2)
            count_tentacles_actual(self.photo.path)
            img = ImagePIL.open(self.photo.path)
            
            # Add markers based on the labels generated by the model
            self.placeInitialMarkers(img.width, img.height)

            # Get tentacle count
            self.count = get_count()
            self.countDisplay.setText(str(get_count()))

            # Delete the new resized.jpg created in the main folder (for some reason)
            if (os.path.exists('resized.jpg')):
                os.remove('resized.jpg')

    def placeInitialMarkers(self, photo_width, photo_height):
        coordinates = get_coordinates()

        for pair in coordinates:
            self.photo.add_marker(pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5))
            self.list.append("({}, {})".format(pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5)))
    
            # ellipse = QGraphicsEllipseItem(
            #     pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5), 15, 15
            # )
            # ellipse.setBrush(QBrush(Qt.yellow))
            # ellipse.setFlag(QGraphicsItem.ItemIsMovable)
            # self.photo.scene.addItem(ellipse)
            # self.photo.marker_count += 1
            # self.photo.markers.append(ellipse)
            # print(self.photo.markers)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.photo.add_marker(x-45, y-125)
            self.list.append("({}, {})".format(x-45, y-125))
            self.countDisplay.setText("{0}".format(self.photo.marker_count))
            
    
    # def addFullMarker(self):
    #     # self.photo.add_marker()
    #     self.photo.mousePressEvent()
    #     self.countDisplay.setText("{0}".format(self.photo.marker_count))
    def removeMarker(self):
        print(self.list)
        print(len(self.list))
        #print(list)
        #print(Image2.print_markers)
        #self.photo.remove_marker()
        #self.countDisplay.setText("{0}".format(self.photo.marker_count))
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())