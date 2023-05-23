from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from basic_styling import *

class InstructionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instructions")
        icon_pixmap = QPixmap("style_images/Actual Final Logo.png")
        self.setWindowIcon(QIcon(icon_pixmap))
        
        layout = QGridLayout()

        self.close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)
        
        self.instructions_Label = QLabel(
            """
Welcome to Capturing Coral Tentacles!

Instructions:
1. Click on Browse to select your image for coral counting.
2. Click Count for the program to generate the markers
    and count. It should take around 5 seconds.
3. To edit the markers, click on any of the markers and click
    Remove or Add Marker. The numerical Count will update 
    automatically.
4. To save your count, click 'Save Picture to Record'. Your 
    Count will now be saved and can be viewed in the Record
    tab.
5. You can delete your own images from the database using the
    delete button and your code. However, you can only see
    other people's entries in a view only window.
6. To reopen an image (yours or someone else's), double click 
    on the entry, or select it and click 'Reopen'.
7. For backup purposes, clicking the 'Export' button will 
    put all the data in a CSV format on your computer, as well
    as a folder of all currently saved images.
        a. Windows: Saved files will be in C:\\temp.
        b. Mac: Saved files will be on the Desktop.

Here are some useful keyboard shortcuts. Some may only work 
when a photo is loaded:

On Main tab:
    Ctrl+O (Windows), Command+O (Mac) - Browse photos
    C - Count
    Double click - Add marker
    R - Remove selected marker
    Ctrl+Z (Windows), Command+Z (Mac) - Undo most recently placed marker
    Ctrl+S (Windows), Command+S (Mac) - Save photo to record
    I - Instructions

On Record tab:
    Delete (Windows), fn delete (Mac) - Delete selected database entry
    Double click on database entry - Reopen
    Ctrl+Enter (Windows), Command+Enter (Mac) in search bar - Search
    Ctrl+R (Windows), Command+R (Mac) - Reload all database entries

Tab - Switch between tabs
Ctrl+W (Windows), Command+W (Mac) - Close application or the
    Instructions or Save window
            """ 
        )
        
        self.closeButton = QPushButton("Close")
        self.closeButton.setCursor(Qt.PointingHandCursor)

        self.instruct_close_shortcut = QShortcut(Qt.Key_Return, self)
        self.instruct_close_shortcut.activated.connect(self.close)
        
        scroll_widget = QWidget()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(750)
        scroll_area.setFixedHeight(600)

        sample_image = QPixmap("style_images/example_coral.JPG")
        sample_image_label = QLabel()
        sample_image_label.setPixmap(sample_image.scaled(700, 400))
        
        layout = QGridLayout()
        layout.addWidget(self.instructions_Label, 0, 0)
        layout.addWidget(QLabel(
"""Note: Make sure your coral image is of a similar size and at least this 
quality!"""), 1, 0)
        layout.addWidget(sample_image_label, 2, 0)
        

        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)
        
        full_layout = QGridLayout()
        full_layout.addWidget(scroll_area, 0, 0)
        full_layout.addWidget(self.closeButton, 1, 0)
        self.setLayout(full_layout)

        self.setStyleSheet(
            "QScrollArea {"
            " border: none;"
            "}"
            + get_basic_styling()
        )