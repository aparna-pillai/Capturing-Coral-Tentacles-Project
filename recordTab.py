from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dotenv import load_dotenv

def recordTabUI(self):
    recordTab = QWidget()
    layout = QGridLayout()

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
    self.searchBar.textChanged.connect(self.searchRecord)

    self.searchGridLayout.addWidget(self.searchLabel, 0, 0)
    self.searchGridLayout.addWidget(self.searchBar, 0, 1)

    layout.addLayout(self.searchGridLayout, 0, 0)
    layout.addWidget(self.directions, 1, 0)
    layout.addWidget(self.tableWidget, 2, 0)

    # self.btnLoad = QPushButton("Load")
    # load_dotenv('config.env')
    # self.btnLoad.clicked.connect(self.DBConnect)
    
    load_dotenv('config.env')
    self.DBConnect()
    
    self.btnDelete = QPushButton("Delete")
    load_dotenv('config.env')
    self.btnDelete.clicked.connect(self.codeBeforeDeleteRow)
    self.btnDeleteAll = QPushButton("Delete All")
    load_dotenv('config.env')
    self.btnDeleteAll.clicked.connect(self.codeBeforeDeleteAllRows)
    self.btnReopen = QPushButton("Reopen")
    self.btnReopen.clicked.connect(self.reopen)
    
    
    self.exportButton = QPushButton("Export")
    load_dotenv('config.env')
    self.exportButton.clicked.connect(self.export)

    self.smGridLayout = QGridLayout()
    #self.smGridLayout.addWidget(self.btnLoad, 0, 0)
    self.smGridLayout.addWidget(self.btnDelete, 0, 0)
    self.smGridLayout.addWidget(self.btnDeleteAll, 1, 0)
    self.smGridLayout.addWidget(self.btnReopen, 2, 0)
    self.smGridLayout.addWidget(self.exportButton, 3, 0)

    layout.addLayout(self.smGridLayout, 2, 1)

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

    # self.btnLoad.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    # )

    self.btnDelete.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #00adb5;"
        "border-left-color: #00adb5;"
        "border-right-color: #00adb5;"
        "border-bottom-color: #00adb5;"
        "color: #112d4e;"
        "width: 150px;"
    )
    
    self.btnDeleteAll.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #00adb5;"
        "border-left-color: #00adb5;"
        "border-right-color: #00adb5;"
        "border-bottom-color: #00adb5;"
        "color: #112d4e;"
    )
    
    self.btnReopen.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #00adb5;"
        "border-left-color: #00adb5;"
        "border-right-color: #00adb5;"
        "border-bottom-color: #00adb5;"
        "color: #112d4e;"
    )
    
    self.exportButton.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #00adb5;"
        "border-left-color: #00adb5;"
        "border-right-color: #00adb5;"
        "border-bottom-color: #00adb5;"
        "color: #112d4e;"
    )
    
    recordTab.setLayout(layout)
    
    return recordTab