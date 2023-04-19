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
from LoginWindow import LoginWindow

from coral_count import count_tentacles_actual, get_count, get_coordinates

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        
        self.move(0,0)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.count = 0
        self.coordinate_list = []
        
        # Create the tab widget with two tabs
        self.tabs = QTabWidget()
        self.general_tab = generalTabUI(self)
        self.record_tab = recordTabUI(self)

        self.tabs.addTab(self.general_tab, "Main")
        self.tabs.addTab(self.record_tab, "Record")
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
         
    def codeBeforeDeleteRow(self):
        print("Hmmmmmm!")
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            print(item)
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
                            print(cell)
                            
            
                    filenameForQuery = item[0].text()
                    
                    self.login = LoginWindow()
                    self.login.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
                    self.login.show()
                    self.login.submitButtonLogin.clicked.connect(lambda: self.deleteRow(currentRow, filenameForQuery, cell))
                    #self.login.submit_shortcut.activated.connect(self.gatheringInfo)
                    
                else:
                    question.close()
            
                    
    def deleteRow(self, currentRow, filenameForQuery, cell):
        
        print("seven malicious hats")
        print(currentRow)
        print(filenameForQuery)
        print(cell)
        
        try:
            mydb = mc.connect(
                host=os.environ.get('HOST'),
                user = os.getenv('NAME'),
                password=os.getenv('PASSWORD'), 
                database=os.getenv('DATABASE')             
            )
            mycursor = mydb.cursor()
            
            mycursor.execute("SELECT users_password FROM users WHERE users_name = '%s'" % cell)
            myresult = mycursor.fetchall()
            print(myresult)
            print(myresult[0])
            str = ''.join(myresult[0])
            print(str)
            if (self.login.codeTextBox.text() == str):
                print("YAAAAAAAAAAAASSSSSS")
            #print(stringOfCode[2:11])
                sql_delete = "DELETE FROM image_info WHERE filename = %s"
                sql_data = (filenameForQuery,)

                mycursor.execute(sql_delete, sql_data)
                self.tableWidget.removeRow(currentRow)
                self.login.close()
            else: 
                QMessageBox.about(self, "Warning", "Wrong Code!")
                self.login.close()
        
            mydb.commit()
            mydb.close()
        except mydb.Error as e:
            print("Failed To Connect to Database")
        
                
    def codeBeforeDeleteAllRows(self):
        question = QMessageBox()
        response = question.question(self,'', "Are you sure you want to delete ALL the rows?", question.Yes | question.No)
                
        if response == question.Yes:
                self.login = LoginWindow()
                self.login.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
                self.login.show()
                self.login.submitButtonLogin.clicked.connect(self.deleteAllRows)
                    #self.login.submit_shortcut.activated.connect(self.gatheringInfo)
                    
        else:
            question.close()
                
    def deleteAllRows(self):
        # question = QMessageBox()
        # response = question.question(self,'', "Are you sure you want to delete ALL the rows?", question.Yes | question.No)
                
        # if response == question.Yes:
            try:
                mydb = mc.connect(
                    host=os.environ.get('HOST'),
                    user = os.getenv('NAME'),
                    password=os.getenv('PASSWORD'), 
                    database=os.getenv('DATABASE')             
                )
                mycursor = mydb.cursor()
                
                mycursor.execute("SELECT users_password FROM users WHERE users_name = '%s'" % os.getenv('ADMIN'))
                myresult = mycursor.fetchall()
                print(myresult)
                print(myresult[0])
                str = ''.join(myresult[0])
                print(str)
                if (self.login.codeTextBox.text() == str):
                    print("YAAAAAAAAAAAASSSSSS")
                
                    mycursor.execute("DELETE FROM image_info")
                
                    mydb.commit()
                    while (self.tableWidget.rowCount() > 0):
                        self.tableWidget.removeRow(0)
                    self.login.close()
                else:
                    QMessageBox.about(self, "Warning", "ONLY THE ADMIN CAN DELETE ALL THE ROWS!")
                    self.login.close()
                mydb.close()
                    
            except mydb.Error as e:
                print("Failed To Connect to Database")
            #self.tableWidget.removeRow(currentRow)
        
    
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
                    item = QTableWidgetItem(str(data))
                    self.tableWidget.setItem(row_number, column_number, item)
                    if column_number == 1:
                        self.user_names.append(item)

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
            QMessageBox.about(self, "Warning", "Check your desktop for the csv file!")
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
                sql =  "SELECT users_name, users_password FROM users WHERE users_name = '%s'" % self.g.get_name()
                mycursor.execute(sql)
                myresult1 = mycursor.fetchall()
                
                if len(myresult1) > 0:
                    print(myresult1)
                    print(myresult1[0])
                    str = ''.join(myresult1[0])
                    print(str)
                    print(str[-10:])
                    print(self.g.get_code())
                    if self.g.get_code() == str[-10:]:
                        print("Hip hip hurray")
                        
                        for i, marker in enumerate(self.photo.markers):
                                self.coordinate_list.append(
                                (str(marker.scenePos()) + ' ; ' + str(self.photo.marker_colors[i]))
                        )

                        coordstring = ' | '.join(self.coordinate_list)
                        
                        mycursor.execute(
                            "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s)", 
                            (
                                self.photo.get_filename(), self.photo.marker_count, 
                                self.g.get_name(), date.today(), 
                                coordstring, self.g.get_notes()
                            )
                        )
                        
                        self.tableWidget.resizeRowsToContents()
                    else: 
                        print("nice try")
                        QMessageBox.about(self, "Warning", "Incorrect name or password!")
                else: 
                    print("nice try")
                    QMessageBox.about(self, "Warning", "Incorrect name or password!")
                #str2 = ''.join(myresult1[1])
                #print(str2)
                
                # if mycursor.fetchone():
                #     print("yeah")
                #     sql2 = "SELECT users_name, users_password FROM users WHERE users_password = '%s'" % self.g
                #     sql2 =  "SELECT users_password FROM users WHERE users_password = '%s'" % self.g.get_code()
                #     mycursor.execute(sql2)
                #     if mycursor.fetchone():
                #         print("oh yeah")
                #         for i, marker in enumerate(self.photo.markers):
                #             self.coordinate_list.append(
                #             (str(marker.scenePos()) + ' ; ' + str(self.photo.marker_colors[i]))
                #         )

                #         coordstring = ' | '.join(self.coordinate_list)
                        
                #         mycursor.execute(
                #             "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s)", 
                #             (
                #                 self.photo.get_filename(), self.photo.marker_count, 
                #                 self.g.get_name(), date.today(), 
                #                 coordstring, self.g.get_notes()
                #             )
                #         )
                        
                #         self.tableWidget.resizeRowsToContents()
                    #print(mycursor.execute(sql))
                #     else:
                #         QMessageBox.about(self, "Warning", "Incorrect name or password!")
                # else:
                #     QMessageBox.about(self, "Warning", "Incorrect name or password!")
                #     print("boo")
            
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
            # self.photo.modelDisplay.setText("Running...")

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

            # self.photo.modelDisplay.setText("{0}".format("Not running anymore"))

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