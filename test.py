import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import platform

import mysql.connector as mc
import os
from dotenv import load_dotenv
from PIL import Image as ImagePIL
from datetime import date, datetime

import pandas as pd

from Image import *
from RecordInfoWindow import RecordInfoWindow
from InstructionsWindow import InstructionsWindow
from generalTab import generalTabUI
from recordTab import recordTabUI

from coral_count import count_tentacles_actual, get_count, get_coordinates

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        self.move(0,0)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 0
        self.coordinate_list = []
        
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

        self.zoomin_shortcut = QShortcut(Qt.Key_Plus, self)
        self.zoomout_shortcut = QShortcut(Qt.Key_Minus, self)

        self.delete_shortcut = QShortcut(Qt.Key_Delete, self)
        self.tab_shortcut = QShortcut(Qt.Key_Tab, self)
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)

        # Connect shortcuts
        self.instructions_shortcut.activated.connect(self.instruct)
        self.count_shortcut.activated.connect(self.countTentacles)
        self.save_shortcut.activated.connect(self.recordInfo)
        self.remove_shortcut.activated.connect(self.photo.remove_marker)
        self.remove_shortcut.activated.connect(self.updateMarkerCount)
        self.undo_shortcut.activated.connect(self.photo.undo_last_marker)
        self.undo_shortcut.activated.connect(self.updateMarkerCount)

        self.zoomin_shortcut.activated.connect(self.photo.zoom_in)
        self.zoomout_shortcut.activated.connect(self.photo.zoom_out)

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
        self.w = InstructionsWindow()
        self.w.closeButton.clicked.connect(self.instructions_close)
        self.w.setGeometry(self.frameGeometry().width(), 0, int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150)
        self.w.show()
        
    def instructions_close(self):
        self.w.close()
         
    def deleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:             
                question = QMessageBox()
                response = question.question(self,'', "Are you sure you want to delete the row?", question.Yes | question.No)
                
                if response == question.Yes:
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
                else:
                    question.close()
                
    def deleteAllRows(self):
        question = QMessageBox()
        response = question.question(self,'', "Are you sure you want to delete ALL the rows?", question.Yes | question.No)
                
        if response == question.Yes:
            try:
                mydb = mc.connect(
                    host=os.environ.get('HOST'),
                    user = os.getenv('NAME'),
                    password=os.getenv('PASSWORD'), 
                    database=os.getenv('DATABASE')             
                )
                mycursor = mydb.cursor()
                
                mycursor.execute("DELETE FROM image_info")
            
                mydb.commit()
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
                mydb.close()
            except mydb.Error as e:
                print("Failed To Connect to Database")
            #self.tableWidget.removeRow(currentRow)
        else:
            question.close()
    
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
    
    def export(self):
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user=os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            
            mycursor = mydb.cursor()

            mycursor.execute("Select filename, tentacle_count, name_of_person, date_uploaded, coordinates_of_markers, notes from image_info")

            result = mycursor.fetchall()
            
            all_filenames = []
            all_tentacle_count = []
            all_name_of_person = []
            all_date_uploaded = []
            all_coordinates_of_markers = []
            all_notes = []
            
            for filename, tentacle_count, name_of_person, date_uploaded, coordinates_of_markers, notes in result:
                all_filenames.append(filename)
                all_tentacle_count.append(tentacle_count)
                all_name_of_person.append(name_of_person)
                all_date_uploaded.append(date_uploaded)
                all_coordinates_of_markers.append(coordinates_of_markers)
                all_notes.append(notes)
            
            dictionary = {
                "FILENAME": all_filenames, "TENTACLE COUNT": all_tentacle_count, 
                "NAME OF PERSON": all_name_of_person, "DATE UPLOADED": all_date_uploaded, 
                "COORDINATES OF MARKERS": all_coordinates_of_markers, "NOTES": all_notes
            }

            df = pd.DataFrame(dictionary)
            if platform.system() == 'Windows':
                df.to_csv("C:\\temp\CountEntries.csv", na_rep="None")
            else:
                df.to_csv(os.path.expanduser("~/Desktop/CountEntries.csv"))
            
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
            
    def recordInfo(self):   
        if self.photo.get_filename() == "":
            QMessageBox.about(self, "Warning", "You did not upload an image!")
        else:
            self.g = RecordInfoWindow()
            self.g.submitButton.clicked.connect(self.gatheringInfo)
            self.g.submit_shortcut.activated.connect(self.gatheringInfo)

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

                for i, marker in enumerate(self.photo.markers):
                    self.coordinate_list.append(marker.scenePos())

                file_actual_name = self.photo.get_filename()[:-4] # cut off the .jpg
                saving_time = datetime.now().strftime("%Y%m%d")
                coord_storage_file = file_actual_name + "_" + saving_time + "_coordinates.txt"
                coordinates_file = open("saved_coordinates/" + coord_storage_file, "w")
                
                for point in self.coordinate_list:
                    coordinates_file.write(str(point)+"\n")
                coordinates_file.close()
                
                mycursor.execute(
                    "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s)", 
                    (
                        self.photo.get_filename(), self.photo.marker_count, 
                        self.g.get_name(), date.today(), 
                        str(coord_storage_file), self.g.get_notes()
                    )
                )
                
                self.tableWidget.resizeRowsToContents()
                mydb.commit()
                
                self.DBConnect()
                self.g.close()
                mydb.close()
                
            except mydb.Error as e:
                print("Failed To Connect to Database")

    def countTentacles(self):
        if (self.photo.get_filename() == ""):
            QMessageBox.about(self, "Warning", "Please upload an image.")
        else:
            # Run the model on the currently displayed photo (in Image)
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
        self.coordinate_list.clear()

        for pair in coordinates:
            self.photo.add_marker(
                pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5), 
                QColor(245, 96, 42)
            )

    def updateMarkerCount(self):
        self.countDisplay.setText("{0}".format(self.photo.marker_count))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.photo.add_marker(x-45, y-125, Qt.yellow)
            self.updateMarkerCount()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()    

    instructions = InstructionsWindow()
    window.activateWindow()

    sys.exit(app.exec_())