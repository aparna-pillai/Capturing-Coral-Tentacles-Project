from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from dotenv import load_dotenv

def recordTabUI(self):
    recordTab = QWidget()
    layout = QGridLayout()

    self.reload_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
    self.reload_shortcut.activated.connect(self.DBConnect)
    # self.reload_shortcut.activated.connect(self.searchBar.setText(""))

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
    
    self.reloadButton.clicked.connect(self.DBConnect)
    self.reloadButton.clicked.connect(self.searchBar.clear)
    self.reload_shortcut.activated.connect(self.searchBar.clear)

    self.searchGridLayout.addWidget(self.searchLabel, 0, 0)
    self.searchGridLayout.addWidget(self.searchBar, 0, 1)
    self.searchGridLayout.addWidget(self.searchButton, 0, 2)
    self.searchGridLayout.addWidget(self.reloadButton, 0, 3)

    layout.addLayout(self.searchGridLayout, 0, 0)
    layout.addWidget(self.directions, 1, 0)
    layout.addWidget(self.tableWidget, 2, 0)
    
    load_dotenv('config.env')
    self.DBConnect()
    
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

    layout.addLayout(self.smGridLayout, 2, 1)

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

    self.searchButton.setStyleSheet(
        "color: white;"
        "width: 150px;"
    
    )
    
    self.reloadButton.setStyleSheet(
        "color: white;"
        "width: 150px;"
    )
    
    self.btnDelete.setStyleSheet(
        "color: white;"
        "width: 150px;"
    )
    
    self.btnDeleteAll.setStyleSheet(
        "border-bottom-color: #00adb5;"
        "color: white;"
    )
    
    self.btnReopen.setStyleSheet(
        "color: white;"
    )
    
    self.exportButton.setStyleSheet(
        "color: white;"
    )
    
    recordTab.setLayout(layout)
    
    return recordTab