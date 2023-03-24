from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from datetime import date

class RecordInfoWindow(QWidget):
    submitButton = None
    
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        
        self.name_of_person_Label = QLabel("Name:")
        self.name_of_person_Display = QLineEdit()
        self.name_of_person_Display.setPlaceholderText("Enter your name here")
        
        self.notes_Label = QLabel("Notes:")
        self.notes_Display = QLineEdit()
        self.notes_Display.setPlaceholderText("Enter any notes you have")
        
        self.date_Label = QLabel("Date Added:")
        self.date_Display = QLabel("{0}".format(date.today()))
        
        self.submitButton = None
        self.submitButton = QPushButton("SUBMIT!")
        self.submit_shortcut = QShortcut(Qt.Key_S, self)
        
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)
        
        layout.addWidget(self.date_Label, 0, 0)
        layout.addWidget(self.date_Display, 0, 1)
        layout.addWidget(self.name_of_person_Label, 1, 0)
        layout.addWidget(self.name_of_person_Display, 1, 1)
        layout.addWidget(self.notes_Label, 2, 0)
        layout.addWidget(self.notes_Display, 2, 1)
        layout.addWidget(self.submitButton, 3, 0)
        
        print(self.name_of_person_Display.text())
        
        self.setLayout(layout)
     
    def get_name(self):
        return self.name_of_person_Display.text()
    
    def get_notes(self):
        return self.notes_Display.text()