from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ViewOnlyTab import *
from CodeDeleteWindow import *
from connectToDatabase import *

from dotenv import load_dotenv
import pandas as pd

class RecordTab(QWidget):
    
    recordDbConnectCalled = pyqtSignal(QTableWidget)
    createViewOnlyTabCall = pyqtSignal(QWidget, str, QPushButton, str)
    reopenOwnEntryCall = pyqtSignal(str, str)

    def __init__(self, username):
        super().__init__()
        self.record_layout = QGridLayout()

        self.record_username = username

        self.directions = QLabel("""
                                You can search by filename, name of person, and date uploaded. 
                                To delete a row, please click directly on the specific filename. 
                                """)

        self.tableWidget = QTableWidget()
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

        scroll_bar = QScrollBar(self)

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

        self.tableWidget.setVerticalScrollBar(scroll_bar)

        self.searchGridLayout = QGridLayout()
        self.searchLabel = QLabel("Search:")
        self.searchBar = QLineEdit()
        self.searchButton = QPushButton("Go")
        self.searchButton.setCursor(Qt.PointingHandCursor)
        self.reloadButton = QPushButton("Reload")
        self.reloadButton.setCursor(Qt.PointingHandCursor)

        self.searchBar.returnPressed.connect(lambda: self.searchRecord(self.searchBar.text()))
        self.searchButton.clicked.connect(lambda: self.searchRecord(self.searchBar.text()))
        
        self.reloadButton.clicked.connect(lambda: self.recordDbConnectCalled.emit(self.tableWidget))
        self.reloadButton.clicked.connect(self.searchBar.clear)

        self.searchGridLayout.addWidget(self.searchLabel, 0, 0)
        self.searchGridLayout.addWidget(self.searchBar, 0, 1)
        self.searchGridLayout.addWidget(self.searchButton, 0, 2)
        self.searchGridLayout.addWidget(self.reloadButton, 0, 3)

        self.record_layout.addLayout(self.searchGridLayout, 0, 0)
        self.record_layout.addWidget(self.directions, 1, 0)
        self.record_layout.addWidget(self.tableWidget, 2, 0)
        
        load_dotenv('config.env')
        self.recordDbConnectCalled.emit(self.tableWidget)
        
        self.btnDelete = QPushButton("Delete")
        self.btnDelete.setCursor(Qt.PointingHandCursor)
        load_dotenv('config.env')
        self.btnDelete.clicked.connect(self.codeBeforeDeleteRow)

        self.btnDeleteAll = QPushButton("Delete All")
        self.btnDeleteAll.setCursor(Qt.PointingHandCursor)
        load_dotenv('config.env')
        self.btnDeleteAll.clicked.connect(self.codeBeforeDeleteAllRows)
        
        self.btnReopen = QPushButton("Reopen")
        self.btnReopen.setCursor(Qt.PointingHandCursor)
        self.btnReopen.clicked.connect(self.reopen)
        
        self.exportButton = QPushButton("Export")
        self.exportButton.setCursor(Qt.PointingHandCursor)
        load_dotenv('config.env')
        self.exportButton.clicked.connect(self.export)

        self.smGridLayout = QGridLayout()
        self.smGridLayout.addWidget(self.btnDelete, 0, 0)
        self.smGridLayout.addWidget(self.btnDeleteAll, 1, 0)
        self.smGridLayout.addWidget(self.btnReopen, 2, 0)
        self.smGridLayout.addWidget(self.exportButton, 3, 0)

        self.record_layout.addLayout(self.smGridLayout, 2, 1)

        # Keyboard shortcuts
        self.reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.delete_shortcut = QShortcut(Qt.Key_Delete, self)

        self.reload_shortcut.activated.connect(
            lambda: self.recordDbConnectCalled.emit(self.tableWidget)
        )
        self.reload_shortcut.activated.connect(self.searchBar.clear)
        self.delete_shortcut.activated.connect(self.codeBeforeDeleteRow)
        self.tableWidget.doubleClicked.connect(self.reopen)

        self.setStyleSheet(
            "QLabel {"
            " color: #00adb5;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 17px;"
            " font-weight: bold;"
            "}"

            "QPushButton {"
            " color: white;"
            " background-color: #3f72af;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 17px;"
            " font-weight: bold;"
            " border-radius: 15px;"
            " padding: 10px 20px;"
            "}"

            "QPushButton:hover {"
            " background-color: #00adb5;"
            "}"

            "QLineEdit {"
            " font-size: 17px;"
            " font-family: 'Lucida Sans Typewriter';"
            "}"

        )

        self.tableWidget.setStyleSheet(
            "border: 1px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
            " font-size: 17px;"
            " font-family: 'Lucida Sans Typewriter';"
        )

        header.setStyleSheet(
            "color: #112d4e;"
            " font-family: 'Lucida Sans Typewriter';"
        )

        self.setLayout(self.record_layout)


    def searchRecord(self, search_text):
        rowsToDelete = []

        for row in range(self.tableWidget.rowCount()):
            columns = [0, 1, 2, 3, 5]
            noMatchFound = True

            for i in columns:
                if search_text.lower() in self.tableWidget.item(row, i).text().lower():
                    noMatchFound = False
            
            if noMatchFound:
                rowsToDelete.append(row)

        # Counter: adjust for the fact that we're removing a row each time
        counter = 0
        for row in rowsToDelete:
            self.tableWidget.removeRow(row - counter)
            counter += 1


    def codeBeforeDeleteRow(self):
        if self.tableWidget.rowCount() > 0:
            currentRow = self.tableWidget.currentRow()
            item = self.tableWidget.selectedItems()
            if (len(item) < 1):
                QMessageBox.about(self, "Warning", "Please select an entry to delete.")
            else:             
                question = QMessageBox()
                response = question.question(
                    self,'', "Are you sure you want to delete the row?", 
                    question.Yes | question.No
                )
                
                if response == question.Yes:
                    headercount = self.tableWidget.columnCount()
                    for x in range(headercount):
                        headertext = self.tableWidget.horizontalHeaderItem(x).text()
                        if headertext == "NAME OF PERSON":
                            nameOfPerson = self.tableWidget.item(currentRow, x).text()  # get cell at row, col
                        if headertext == "DATE UPLOADED":
                            dateUploaded = self.tableWidget.item(currentRow, x).text()
                    
                    filenameForQuery = item[0].text()
                    
                    self.codeDelete = CodeDeleteWindow()
                    self.codeDelete.setGeometry(
                        int(self.frameGeometry().width()/2) - 150, 
                        int(self.frameGeometry().height()/2) - 150, 300, 300
                    )
                    self.codeDelete.show()
                    self.codeDelete.submitButtonLogin.clicked.connect(
                        lambda: self.deleteRow(
                            currentRow, filenameForQuery, nameOfPerson, dateUploaded
                        )
                    )

                    self.codeDelete.submit_shortcut.activated.connect(
                        lambda: self.deleteRow(
                            currentRow, filenameForQuery, nameOfPerson, dateUploaded
                        )
                    )
                    
                else:
                    question.close()

    def deleteRow(self, currentRow, filenameForQuery, nameOfPerson, dateUploaded):        
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % nameOfPerson)
            myresult = mycursor.fetchall()

            str = ''.join(myresult[0])

            mycursor.execute(
                "SELECT users_code FROM users WHERE users_name = '%s'" % os.getenv('ADMIN')
            )
            myresult_admin = mycursor.fetchall()
            str_admin = ''.join(myresult_admin[0])

            if (self.codeDelete.codeTextBox.text() == str 
            or self.codeDelete.codeTextBox.text() == str_admin):
                sql_delete = "DELETE FROM image_info WHERE filename = %s and date_uploaded = %s"
                sql_data = (filenameForQuery, dateUploaded)

                mycursor.execute(sql_delete, sql_data)
                self.tableWidget.removeRow(currentRow)
                self.codeDelete.close()
            elif (self.codeDelete.codeTextBox.text() == ""):
                QMessageBox.about(self, "Warning", "Please enter a code.")
                self.codeDelete.close()
                self.codeBeforeDeleteRow()
            else: 
                QMessageBox.about(self, "Warning", "Wrong code.")
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
            self.codeDeleteAllWindow.label.setText("Enter ADMIN code:")
            self.codeDeleteAllWindow.setGeometry(
                int(self.frameGeometry().width()/2) - 150, 
                int(self.frameGeometry().height()/2) - 150, 300, 300
            )
            self.codeDeleteAllWindow.show()

            self.codeDeleteAllWindow.submitButtonLogin.clicked.connect(self.deleteAllRows) 
            self.codeDeleteAllWindow.submit_shortcut.activated.connect(self.deleteAllRows)   
        else:
            question.close()

    def deleteAllRows(self):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            
            mycursor.execute(
                "SELECT users_code FROM users WHERE users_name = '%s'" % os.getenv('ADMIN')
            )
            myresult = mycursor.fetchall()

            str = ''.join(myresult[0])

            if (self.codeDeleteAllWindow.codeTextBox.text() == str):
                mycursor.execute("DELETE FROM image_info")
            
                mydb.commit()
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)
                self.codeDeleteAllWindow.close()
            else:
                QMessageBox.about(self, "Warning", "Wrong code.\nOnly the admin can delete all the rows.")
                self.codeDeleteAllWindow.close()
                
            
            mydb.close()
                
        except mydb.Error as e:
            print("Failed To Connect to Database")

    def reopen(self):
        if not self.tableWidget.selectedItems():
            QMessageBox.about(self, "Warning", "Please select an entry to reopen.")
        else:
            try:
                mydb = connectToDatabase()
                mycursor = mydb.cursor()
                
                item = self.tableWidget.selectedItems()
                row = item[0].row()
                filenameForQuery = item[0].text()
                
                mycursor.execute("SELECT * FROM image_info WHERE filename='%s'" % filenameForQuery)
                
                myresult = mycursor.fetchone()[6]
                tentacleCount = self.tableWidget.item(row, 1).text()
                ownerName = self.tableWidget.item(row, 2).text()
                dateUploaded = self.tableWidget.item(row, 3).text()
                coordinates = self.tableWidget.item(row, 4).text()
                ownerNotes = self.tableWidget.item(row, 5).text()

                with open(filenameForQuery, "wb") as file:
                    file.write(myresult)
                    file.close()
                
                if (ownerName != self.record_username):
                    self.view_tab = ViewOnlyTab(
                        filenameForQuery, tentacleCount, 
                        coordinates, ownerName, ownerNotes, dateUploaded
                    )
                    self.closeViewTabButton = QPushButton()
                    self.closeViewTabButton.setCursor(Qt.PointingHandCursor)
                    self.closeViewTabButton.setIcon(
                        self.style().standardIcon(QStyle.SP_TitleBarCloseButton)
                    )
                    self.closeViewTabButton.setIconSize(QSize(10, 10))
                    self.closeViewTabButton.setStyleSheet(
                        "border: none;"
                        "color: white;"
                        "background-color: none;"
                        "padding: 0px;"
                    )
                    
                    viewTabText = "View - " + ownerName + ", " + filenameForQuery + " | " + dateUploaded

                    self.createViewOnlyTabCall.emit(
                        self.view_tab, viewTabText, self.closeViewTabButton, filenameForQuery
                    )
                    
                else:
                    self.reopenOwnEntryCall.emit(filenameForQuery, coordinates)

                mydb.close()
            
            except mydb.Error as e:
                print("Failed To Connect to Database")

    def export(self):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor(buffered=True) # Needed for saving all pictures to desktop
            mycursor.execute(
                "Select filename, tentacle_count, name_of_person, date_uploaded, coordinates_of_markers, notes from image_info"
            )

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
            windows_dirname = "C:\\temp\Capturing Coral Images"
            mac_dirname = os.path.expanduser("~/Desktop/Capturing Coral Images")

            if platform.system() == 'Windows':
                df.to_csv("C:\\temp\CoralCountEntries.csv", na_rep="None")
                if not os.path.exists(windows_dirname):
                    os.mkdir(windows_dirname)
            else:
                df.to_csv(os.path.expanduser("~/Desktop/CoralCountEntries.csv"))
                if not os.path.exists(mac_dirname):
                    os.mkdir(mac_dirname)
            
            # Save all pictures to the person's computer. [*set()] clears duplicates.
            for filename in [*set(all_filenames)]:
                mycursor.execute("SELECT * FROM image_info WHERE filename='%s'" % filename)
                myresult = mycursor.fetchone()[6]

                if platform.system() == 'Windows':
                    with open(os.path.join(windows_dirname, filename), "wb") as file:
                        file.write(myresult)
                        file.close()
                else:
                    with open(os.path.join(mac_dirname, filename), "wb") as file:
                        file.write(myresult)
                        file.close()                

            QMessageBox.about(self, "Notice", 
                """Check your desktop for the csv file and all image files.
\n(Windows: See temp folder in C: drive)"""
            )
            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")