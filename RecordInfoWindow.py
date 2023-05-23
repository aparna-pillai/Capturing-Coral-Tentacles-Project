from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from basic_styling import *

from datetime import datetime

class RecordInfoWindow(QWidget):
    submitButton = None
    
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Save Image to Record")
        icon_pixmap = QPixmap("style_images/Actual Final Logo.png")
        self.setWindowIcon(QIcon(icon_pixmap))
        layout = QGridLayout()

        self.username = username
        self.username_Label = QLabel("Name: " + self.username)
        
        self.date_Label = QLabel("Date Added:")
        self.date_Display = QLabel("{0}".format(datetime.today()))
        self.dateGridLayout = QGridLayout()
        self.dateGridLayout.addWidget(self.date_Label, 0, 0)
        self.dateGridLayout.addWidget(self.date_Display, 0, 1)
        
        self.notes_Label = QLabel("Notes:")
        self.notes_Display = QLineEdit()
        self.notes_Display.setPlaceholderText("Enter notes on this entry")
        self.notesGridLayout = QGridLayout()
        self.notesGridLayout.addWidget(self.notes_Label, 0, 0)
        self.notesGridLayout.addWidget(self.notes_Display, 0, 1)
        
        self.submitButton = None
        self.submitButton = QPushButton("Submit")
        self.submitButton.setCursor(Qt.PointingHandCursor)
        self.submit_shortcut = QShortcut(Qt.Key_Return, self)
        
        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)
        
        layout.addWidget(self.username_Label, 0, 0)
        layout.addLayout(self.dateGridLayout, 1, 0)
        layout.addLayout(self.notesGridLayout, 2, 0)
        layout.addWidget(self.submitButton, 3, 0)
        
        self.setLayout(layout)

        self.setStyleSheet(get_basic_styling())
     
    def get_name(self):
        return self.username
    
    def get_code(self):
        return self.code_Display.text()
    
    def get_notes(self):
        return self.notes_Display.text()