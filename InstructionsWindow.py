from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class InstructionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QGridLayout()
        
        self.instructions_Label = QLabel(
            '''
            1. Click on Browse to select your image for coral counting.
            2. Click Count for the program to generate the markers
                and count.
            3. To edit the markers, click on any of the markers and click
                Remove or Add Marker. The numerical Count will update 
                automatically.
            4. To save your count, click Save Count. Your Count will now 
                be saved in the Record/Log.
            5. You can delete the saved count from the Record by 
                clicking Delete Count.
            6. Here are some useful keyboard shortcuts:

            On Main tab:
                Ctrl+O (Windows), Command+O (Mac) - Browse photos
                C - Count
                Click - Add marker
                R - Remove selected marker
                Ctrl+Z (Windows), Command+Z (Mac) - Undo most 
                    recent marker
                Ctrl+S (Windows), Command+S (Mac) - Save photo 
                    to record
                I - Instructions

            On Record tab:
                Enter (Windows), return (Mac) - Load from database
                Delete (Windows), fn delete (Mac) - Delete selected 
                    database entry

            Tab - Switch between tabs
            Ctrl+W (Windows), Command+W (Mac) - Close application
            ''' 
        )
        
        self.closeButton = QPushButton("CLOSE!")

        layout.addWidget(self.instructions_Label, 0, 0)
        layout.addWidget(self.closeButton, 1, 0)
        self.setLayout(layout)