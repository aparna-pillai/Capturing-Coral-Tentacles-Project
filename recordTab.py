from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dotenv import load_dotenv

def recordTabUI(self):
        recordTab = QWidget()
        layout = QGridLayout()

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
 
        layout.addWidget(self.tableWidget, 0, 0) 

        # self.btnLoad = QPushButton("Load")
        # load_dotenv('config.env')
        # self.btnLoad.clicked.connect(self.DBConnect)
        
        load_dotenv('config.env')
        self.DBConnect()
        
        self.btnDelete = QPushButton("Delete")
        load_dotenv('config.env')
        self.btnDelete.clicked.connect(self.deleteRow)
        self.btnDeleteAll = QPushButton("Delete All")
        load_dotenv('config.env')
        self.btnDeleteAll.clicked.connect(self.deleteAllRows)
        
        self.exportButton = QPushButton("Export")
        load_dotenv('config.env')
        self.exportButton.clicked.connect(self.export)

        self.smGridLayout = QGridLayout()
        #self.smGridLayout.addWidget(self.btnLoad, 0, 0)
        self.smGridLayout.addWidget(self.btnDelete, 0, 0)
        self.smGridLayout.addWidget(self.btnDeleteAll, 0, 1)
        self.smGridLayout.addWidget(self.exportButton, 1, 0)

        layout.addLayout(self.smGridLayout, 1, 0)

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
        )
        
        self.btnDeleteAll.setStyleSheet(
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