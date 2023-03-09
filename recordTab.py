from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from RecordInfoWindow import *
from dotenv import load_dotenv

from generalTab import GeneralTab

class RecordTab(QWidget):

    def __init__(self):
        super().__init__()

        # Layout and setup
        self.recordLayout = QGridLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["FILENAME", "TENTACLE COUNT", "NAME OF PERSON", "DATE UPLOADED", "COORDINATES OF MARKERS", "NOTES"]) 
        
        self.header = self.tableWidget.horizontalHeader()       
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)
        self.header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        
        self.tableWidget.setObjectName("tableWidget")
        
        self.scroll_bar = QScrollBar(self)

        # setting vertical scroll bar to it
        self.tableWidget.setVerticalScrollBar(self.scroll_bar)
 
        self.recordLayout.addWidget(self.tableWidget, 0, 0) 

        self.btnLoad = QPushButton("Load")
        load_dotenv('config.env')
        self.btnLoad.clicked.connect(self.DBConnect)
        self.btnDelete = QPushButton("Delete")
        load_dotenv('config.env')
        self.btnDelete.clicked.connect(self.deleteRow)

        self.smGridLayout = QGridLayout()
        self.smGridLayout.addWidget(self.btnLoad, 0, 0)
        self.smGridLayout.addWidget(self.btnDelete, 0, 1)

        self.recordLayout.addLayout(self.smGridLayout, 1, 0)

        # Stylesheets
        self.scroll_bar.setStyleSheet(
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

        self.tableWidget.setStyleSheet(
            "border: 1px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )

        self.header.setStyleSheet(
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

        self.setLayout(self.recordLayout)

    
    def recordInfo(self):
        if self.photo.get_filename() == "":
            QMessageBox.about(self, "Warning", "You did not upload an image!")
        else:
            GeneralTab.get_g = RecordInfoWindow()
            GeneralTab.get_g.submitButton.clicked.connect(self.gatheringInfo)
            GeneralTab.get_g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
            GeneralTab.get_g.show()

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
                    GeneralTab.get_photo_object.get_filename(), 
                    GeneralTab.get_photo_object.marker_count, 
                    GeneralTab.get_g.get_name(), 
                    date.today(), 
                    coordString, 
                    GeneralTab.get_g.get_notes()
                )
            )
            
            self.tableWidget.resizeRowsToContents()
            mydb.commit()

            print("Coordinate list length:", len(self.list))
            GeneralTab.get_g.close()
            mydb.close()
            
        except mydb.Error as e:
            print("Failed To Connect to Database")

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