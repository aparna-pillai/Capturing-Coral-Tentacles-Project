# Source for image upload PyQt code:
# https://stackoverflow.com/questions/60614561/how-to-ask-user-to-input-an-image-in-pyqt5
# Source for counting dots
# https://stackoverflow.com/questions/60603243/detect-small-dots-in-image 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mysql.connector as mc
import os
from dotenv import load_dotenv
from PIL import Image as ImagePIL
from datetime import date

from Image import *
from RecordInfoWindow import RecordInfoWindow
from generalTab import generalTabUI
from recordTab import recordTabUI

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
        general_tab = generalTabUI(self)
        record_tab = recordTabUI(self)

        self.tabs.addTab(general_tab, "Main")
        self.tabs.addTab(record_tab, "Record")
        layout.addWidget(self.tabs)

        # Keyboard shortcuts
        self.instructions_shortcut = QShortcut(Qt.Key_I, self)
        self.count_shortcut = QShortcut(Qt.Key_C, self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.remove_shortcut = QShortcut(Qt.Key_R, self)
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)

        self.load_shortcut = QShortcut(Qt.Key_Return, self)
        self.delete_shortcut = QShortcut(Qt.Key_Delete, self)
        self.tab_shortcut = QShortcut(Qt.Key_Tab, self)
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)

        self.instructions_shortcut.activated.connect(self.instruct)
        self.count_shortcut.activated.connect(self.countTentacles)
        self.save_shortcut.activated.connect(self.recordInfo)
        self.remove_shortcut.activated.connect(self.photo.remove_marker)
        self.remove_shortcut.activated.connect(self.updateMarkerCount)
        self.undo_shortcut.activated.connect(self.photo.undo_last_marker)
        self.undo_shortcut.activated.connect(self.updateMarkerCount)

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
    
    def instruct(self):
        msg = QMessageBox.about(
            self, "Instructions", 
            '''
            Instructions :
            1. Click on Browse to select your image for coral counting.
            2. Click Count for the program to generate the markers
               and count.
            3. To edit the markers, click on any of the markers and click
               Remove or Add Marker. The numerical Count will update 
               automatically.
            4. To save your count, click Save Count. Your Count will now 
               be saved in the Record/Log.
            5. You can delete the saved count from the Record by 
               clicking Delete Count.
            6. Here are some useful keyboard shortcuts:

            On Main tab:
                Ctrl+O - Browse photos
                C - Count
                Click - Add marker
                R - Remove selected marker
                Ctrl+Z (Windows), Command+Z (Mac) - Undo most 
                    recent marker
                Ctrl+S (Windows), Command+S (Mac) - Save photo 
                    to record
                I - Instructions

            On Record tab:
                Enter (Windows), return (Mac) - Load from database
                Delete (Windows), fn delete (Mac) - Delete selected 
                    database entry

            Tab - Switch between tabs
            Ctrl+W (Windows), Command+W (Mac) - Close application
            ''' 
        )
        return msg
 
    def deleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:
                filenameForQuery = item[0].text()
                
                try:
                    mydb = mc.connect(
                        host=os.environ.get('HOST'),
                        user = os.getenv('NAME'),
                        password=os.getenv('PASSWORD'), 
                        database=os.getenv('DATABASE')             
                    )
                    mycursor = mydb.cursor()
                    
                    sql_delete = "DELETE FROM image_info WHERE filename = %s"
                    sql_data = (filenameForQuery,)

                    mycursor.execute(sql_delete, sql_data)
                
                    mydb.commit()
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
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
            
    def recordInfo(self):   # checked parameter? Is it needed?
        if self.photo.get_filename() == "":
            QMessageBox.about(self, "Warning", "You did not upload an image!")
        else:
            self.g = RecordInfoWindow()
            self.g.submitButton.clicked.connect(self.gatheringInfo)
            self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
            self.g.show()
            
    def gatheringInfo(self):  
            try:
                mydb = mc.connect(
                    host=os.environ.get('HOST'),
                    user=os.getenv('NAME'),
                    password=os.getenv('PASSWORD'), 
                    database=os.getenv('DATABASE')             
                )
                
                mycursor = mydb.cursor()
                coordString = ''.join(self.list)
                
                mycursor.execute(
                    "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s)", 
                    (
                        self.photo.get_filename(), self.photo.marker_count, 
                        self.g.get_name(), date.today(), coordString, self.g.get_notes()
                    )
                )
                
                self.tableWidget.resizeRowsToContents()
                mydb.commit()

                # There's a discrepancy with how many markers are recorded in self.list
                print("Coordinate list length:", len(self.photo.markers))
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

            # Delete the new resized.jpg created in the main folder
            if (os.path.exists('resized.jpg')):
                os.remove('resized.jpg')

    def placeInitialMarkers(self, photo_width, photo_height):
        coordinates = get_coordinates()

        # Clear out all old results
        self.photo.marker_count = 0
        self.photo.markers.clear()
        self.list.clear()

        for pair in coordinates:
            self.photo.add_marker(
                pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5), 
                QColor(245, 96, 42)
            )
            self.list.append("({}, {})".format(pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5)))
    

    def updateMarkerCount(self):
        self.countDisplay.setText("{0}".format(self.photo.marker_count))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.photo.add_marker(x-45, y-125, Qt.yellow)
            self.list.append("({}, {})".format(x-45, y-125))
            self.updateMarkerCount()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())