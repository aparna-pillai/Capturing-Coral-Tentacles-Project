import platform
import os
import os.path
import PIL.Image
import pandas as pd

from dotenv import load_dotenv
from datetime import date

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Image import *
from RecordInfoWindow import *
from InstructionsWindow import *
from generalTab import *
from recordTab import *
from viewOnlyTab import *
from CodeDeleteWindow import *
from connectToDatabase import *
from coral_count import *

# https://www.youtube.com/watch?v=NwvTh-gkdfs 

class Coral_Window(QWidget):
    
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        
        self.username = username
        
        self.username_Label = QLabel("Welcome " + self.username.upper() + "!")
                
        self.move(0,0)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 0
        self.coordinate_list = []

        # Sample photo & coordinates for view-only tab testing
        test_image = "IMG-6268.JPG"
        test_coordinates = "PyQt5.QtCore.QPointF(317.0, 276.0) ; Green | PyQt5.QtCore.QPointF(401.0, 214.0) ; Purple | PyQt5.QtCore.QPointF(452.0, 277.0) ; Yellow"
        
        # Create the tab widget with two tabs
        self.tabs = QTabWidget()
        self.general_tab = generalTabUI(self)
        self.record_tab = recordTabUI(self)
        self.view_tab = viewOnlyTabUI(self, test_image, test_coordinates)

        self.tabs.addTab(self.general_tab, "Main")
        self.tabs.addTab(self.record_tab, "Record")
        self.tabs.addTab(self.view_tab, "View")
        layout.addWidget(self.username_Label)
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
        
    def switchTabs(self):
        if self.tabs.isTabEnabled(0):
            self.tabs.setTabEnabled(1, True)
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(2, False)
        elif self.tabs.isTabEnabled(1):
            self.tabs.setTabEnabled(2, True)
            self.tabs.setTabEnabled(0, False)
            self.tabs.setTabEnabled(1, False)
        else:
            self.tabs.setTabEnabled(0, True)
            self.tabs.setTabEnabled(1, False)
            self.tabs.setTabEnabled(2, False)
    
    def instruct(self):
        self.w = InstructionsWindow()
        self.w.closeButton.clicked.connect(self.instructions_close)
        self.w.setGeometry(self.frameGeometry().width(), 0, int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150)
        self.w.show()
        
    def instructions_close(self):
        self.w.close()
         
    def codeBeforeDeleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:             
                question = QMessageBox()
                response = question.question(self,'', "Are you sure you want to delete the row?", question.Yes | question.No)
                
                if response == question.Yes:
                    headercount = self.tableWidget.columnCount()
                    for x in range(headercount):
                        headertext = self.tableWidget.horizontalHeaderItem(x).text()
                        if headertext == "NAME OF PERSON":
                            cell = self.tableWidget.item(currentRow, x).text()  # get cell at row, col
                            
            
                    filenameForQuery = item[0].text()
                    
                    self.codeDelete = CodeDeleteWindow()
                    self.codeDelete.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
                    self.codeDelete.show()
                    self.codeDelete.submitButtonLogin.clicked.connect(lambda: self.deleteRow(currentRow, filenameForQuery, cell))
                    #self.login.submit_shortcut.activated.connect(self.gatheringInfo)
                    
                else:
                    question.close()
    
                    
    def deleteRow(self, currentRow, filenameForQuery, cell):        
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % cell)
            myresult = mycursor.fetchall()

            str = ''.join(myresult[0])

            if (self.codeDelete.codeTextBox.text() == str):
                sql_delete = "DELETE FROM image_info WHERE filename = %s"
                sql_data = (filenameForQuery,)

                mycursor.execute(sql_delete, sql_data)
                self.tableWidget.removeRow(currentRow)
                self.codeDelete.close()
            else: 
                QMessageBox.about(self, "Warning", "Wrong Code!")
                self.codeDelete.close()
        
            mydb.commit()
            mydb.close()
        except mydb.Error as e:
            print("Failed To Connect to Database")
        
                
    def codeBeforeDeleteAllRows(self):
        question = QMessageBox()
        response = question.question(self,'', "Are you sure you want to delete ALL the rows?", question.Yes | question.No)
                
        if response == question.Yes:
            self.codeDeleteAllWindow = CodeDeleteWindow()
            self.codeDeleteAllWindow.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
            self.codeDeleteAllWindow.show()
            self.codeDeleteAllWindow.submitButtonLogin.clicked.connect(self.deleteAllRows)    
        else:
            question.close()
                
    def deleteAllRows(self):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % os.getenv('ADMIN'))
            myresult = mycursor.fetchall()
            
            print(myresult)
            print(myresult[0])

            str = ''.join(myresult[0])

            if (self.codeDeleteAllWindow.codeTextBox.text() == str):
                mycursor.execute("DELETE FROM image_info")
            
                mydb.commit()
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
                self.codeDeleteAllWindow.close()
            else:
                QMessageBox.about(self, "Warning", "ONLY THE ADMIN CAN DELETE ALL THE ROWS!")
                self.codeDeleteAllWindow.close()
                
            
            mydb.close()
                
        except mydb.Error as e:
            print("Failed To Connect to Database")

        
    
    def DBConnect(self):
        try:
            mydb = connectToDatabase()
            
            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM image_info")

            result = mycursor.fetchall()
        
            self.tableWidget.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    self.tableWidget.setItem(row_number, column_number, item)

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")

    def searchRecord(self, search_text):
        if search_text == "":
            self.DBConnect()
        else:
            # self.DBConnect()
            # ^ This will ensure it works all the time, but it's very laggy
            rowsToDelete = []

            for row in range(self.tableWidget.rowCount()):
                item_name = self.tableWidget.item(row, 2).text().lower()
                item_file = self.tableWidget.item(row, 0).text().lower()
                item_date = self.tableWidget.item(row, 3).text().lower()
                item_notes = self.tableWidget.item(row, 5).text().lower()

                if (search_text.lower() not in item_name and search_text.lower() not in item_file 
                    and search_text.lower() not in item_date and search_text.lower() not in item_notes):
                        rowsToDelete.append(row)

            # Counter: adjust for the fact that we're removing a row each time
            counter = 0
            for row in rowsToDelete:
                self.tableWidget.removeRow(row-counter)
                counter += 1
    
    def reopen(self):
        self.tabs.setCurrentIndex(2)
        try:
            mydb = connectToDatabase()
            
            mycursor = mydb.cursor()
            
            item = self.tableWidget.selectedItems()
            filenameForQuery = item[0].text()
            
            mycursor.execute("SELECT * FROM image_info WHERE filename='%s'" % filenameForQuery)
            
            myresult = mycursor.fetchone()[6]

            storefilepath = "NewImage.jpg".format(str(filenameForQuery))
            
            with open(storefilepath, "wb") as file:
                file.write(myresult)
                file.close()
                
            im = PIL.Image.open(r"%s" % storefilepath)
            im.show()
            
            mydb.commit()
            mydb.close()
            
        except mydb.Error as e:
           print("Failed To Connect to Database")
                    
    def export(self):
        try:
            mydb = connectToDatabase()
            
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
            QMessageBox.about(self, "Warning", "Check your desktop for the csv file!")
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")
            
    def recordInfo(self):   
        if not self.photo.get_filename():
            QMessageBox.about(self, "Warning", "You did not upload an image!")
        else:
            self.g = RecordInfoWindow(self.username)
            self.g.submitButton.clicked.connect(self.gatheringInfo)
            self.g.submit_shortcut.activated.connect(self.gatheringInfo)

            self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
            self.g.show()
            
    def convertToBinaryData(self, filename):
    # Convert digital data to binary format
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
            
    def gatheringInfo(self):  
            try:
                mydb = connectToDatabase()
                
                    
                mycursor = mydb.cursor()
                        
                for i, marker in enumerate(self.photo.markers):
                    self.coordinate_list.append(
                        str(marker.scenePos()) + ' ; ' + str(self.photo.marker_colors[i])
                    )

                coordstring = ' | '.join(self.coordinate_list)

                with open(self.photo.get_path(), "rb") as file:
                    binaryData = file.read()       
                                            
                mycursor.execute(
                    "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (
                        self.photo.get_filename(), self.photo.marker_count, 
                        self.username, date.today(), 
                        coordstring, self.g.get_notes(), binaryData
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
            img = PIL.Image.open(self.photo.path)
            
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
        self.updateMarkerCount()
        self.photo.markers.clear()
        self.coordinate_list.clear()

        for pair in coordinates:
            self.photo.add_marker(
                pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5), 
                "YOLO Red"
            )

    def updateMarkerCount(self):
        self.countDisplay.setText("{0}".format(self.photo.marker_count))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.photo.add_marker(x-45, y-125, "Yellow")
            self.updateMarkerCount()