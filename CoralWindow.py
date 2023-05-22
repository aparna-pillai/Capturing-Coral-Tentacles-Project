import os
import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from GeneralTab import *
from RecordTab import *
from connectToDatabase import *

class Coral_Window(QWidget):

    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Capturing Coral Tentacles")
        
        self.username = username
        self.username_Label = QLabel("Welcome, " + self.username + "!")
                
        self.move(0,0)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.closeAllViewTabsButton = QPushButton("Close All View Only Tabs")
        self.closeAllViewTabsButton.setCursor(Qt.PointingHandCursor)
        self.closeAllViewTabsButton.clicked.connect(lambda: self.closeViewOnlyTabs("All"))

        self.chooseTab_Label = QLabel("Navigate to Tab:")
        self.tabChooseMenu = QComboBox()
        self.tabChooseMenu.addItems(["Main", "Record"])
        self.tabChooseMenu.activated[str].connect(self.navigateToTab)

        self.tabChoiceBoxLayout = QHBoxLayout()
        self.tabChoiceBoxLayout.addWidget(self.chooseTab_Label, 1)
        self.tabChoiceBoxLayout.addWidget(self.tabChooseMenu, 3, Qt.AlignLeft)
        self.tabChoiceBoxLayout.addWidget(self.closeAllViewTabsButton, 5)
        
        # Create the tab widget with two tabs
        self.tabs = QTabWidget()
        self.record_tab = RecordTab(self.username)
        self.general_tab = GeneralTab(self.tabs, self.username, self.record_tab.tableWidget)
        self.tabs.addTab(self.general_tab, "Main")
        self.tabs.addTab(self.record_tab, "Record")

        self.general_tab.generalDbConnectCalled.connect(self.DBConnect)
        self.record_tab.recordDbConnectCalled.connect(self.DBConnect)
        self.record_tab.createViewOnlyTabCall.connect(self.addViewOnlyTab)
        self.record_tab.reopenOwnEntryCall.connect(self.general_tab.reopenOwnEntry)

        # Initial connection, get data for display in Record tab immediately
        self.DBConnect(self.record_tab.tableWidget)

        layout.addWidget(self.username_Label)
        layout.addLayout(self.tabChoiceBoxLayout)
        layout.addWidget(self.tabs)

        self.tabs.setStyleSheet(
            "font-family: 'Lucida Sans Typewriter';"
            "font-size: 15px;"
        )

        self.username_Label.setStyleSheet(
            "color: #11e5f0;"
        )

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

            "QComboBox {"
            " border: 3px solid;"
            " border-top-color: #00adb5;"
            " border-left-color: #00adb5;"
            " border-right-color: #00adb5;"
            " border-bottom-color: #00adb5;"
            " color: #112d4e;" 
            " padding-right: 8px;"
            " padding-left: 2px;"
            " width: 400px;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 14px;"
            "}"

        )

        self.tab_shortcut = QShortcut(Qt.Key_Tab, self)
        self.tab_shortcut.activated.connect(self.switchTabs)
        

    def DBConnect(self, tableWidgetParameter):
        try:
            mydb = connectToDatabase()
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM image_info")

            result = mycursor.fetchall()
        
            tableWidgetParameter.setRowCount(0)

            for row_number, row_data in enumerate(result):
                tableWidgetParameter.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    # Only filename should be selectable
                    if column_number != 0:
                        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)

                    tableWidgetParameter.setItem(row_number, column_number, item)

            mydb.close()
        except mydb.Error as e:
           print("Failed To Connect to Database")

    def addViewOnlyTab(self, viewTabObject, viewTabText, viewTabButton, fileToDelete):
        i = 0
        while i < self.tabs.count():
            if self.tabs.tabText(i) == viewTabText:
                self.tabs.setCurrentIndex(i)

                if (os.path.exists(fileToDelete)):
                    os.remove(fileToDelete) 

                return
            else:
                i += 1

        self.tabs.addTab(viewTabObject, viewTabText)
        self.tabChooseMenu.addItem(viewTabText)
        self.tabs.tabBar().setTabButton(
            self.tabs.count()-1, QTabBar.RightSide, viewTabButton
        )
        self.tabs.setTabToolTip(self.tabs.count()-1, viewTabText)
        self.tabs.setCurrentIndex(self.tabs.count()-1)

        viewTabButton.clicked.connect(lambda: self.closeViewOnlyTabs(viewTabText))

        if (os.path.exists(fileToDelete)):
            os.remove(fileToDelete) 


    # Tab Navigation
    def switchTabs(self):
        if self.tabs.currentIndex() == (self.tabs.count() - 1):
            self.tabs.setCurrentIndex(0)
            self.general_tab.updateMarkerCount()
        else:
            self.tabs.setCurrentIndex(self.tabs.currentIndex() + 1)
            if self.tabs.currentIndex() == 1:
                self.DBConnect(self.record_tab.tableWidget)
                            
    def navigateToTab(self, tab_name):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == tab_name:
                self.tabs.setCurrentIndex(i)
                return

    def closeViewOnlyTabs(self, text):
        if text != "All":
            i = 0
            while i < self.tabs.count():
                if self.tabs.tabText(i) == text:
                    self.tabs.removeTab(i)
                    self.tabChooseMenu.removeItem(i)
                    return
                else:
                    i += 1
        else:
            while self.tabs.count() > 2:
                self.tabs.removeTab(2)
                self.tabChooseMenu.removeItem(2)
