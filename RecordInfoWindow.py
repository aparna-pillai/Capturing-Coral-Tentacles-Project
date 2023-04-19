from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from datetime import date

class RecordInfoWindow(QWidget):
    submitButton = None
    
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        
        self.name_of_person_Label = QLabel("Username:")
        self.name_of_person_Display = QLineEdit()
        self.name_of_person_Display.setPlaceholderText("Enter your username here")
        
        self.code_Label = QLabel("Code:")
        self.code_Display = QLineEdit()
        self.code_Display.setPlaceholderText("Enter your code here")
        
        self.notes_Label = QLabel("Notes:")
        self.notes_Display = QLineEdit()
        self.notes_Display.setPlaceholderText("Enter any notes you have")
        
        self.date_Label = QLabel("Date Added:")
        self.date_Display = QLabel("{0}".format(date.today()))
        
        self.submitButton = None
        self.submitButton = QPushButton("SUBMIT!")
        self.submit_shortcut = QShortcut(Qt.Key_Return, self)
        
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)
        
        layout.addWidget(self.date_Label, 0, 0)
        layout.addWidget(self.date_Display, 0, 1)
        layout.addWidget(self.name_of_person_Label, 1, 0)
        layout.addWidget(self.name_of_person_Display, 1, 1)
        layout.addWidget(self.code_Label, 2, 0)
        layout.addWidget(self.code_Display, 2, 1)
        layout.addWidget(self.notes_Label, 3, 0)
        layout.addWidget(self.notes_Display, 3, 1)
        layout.addWidget(self.submitButton, 4, 0)
        
        print(self.name_of_person_Display.text())
        
        self.setLayout(layout)
     
    def get_name(self):
        return self.name_of_person_Display.text()
    
    def get_code(self):
        return self.code_Display.text()
    
    def get_notes(self):
        return self.notes_Display.text()