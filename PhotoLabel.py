from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n (Image will appear here) \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #00adb5;
            color: #3f72af;
        }''')

        self.setToolTip("To add markers, double click on coral photo.")
        
    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)