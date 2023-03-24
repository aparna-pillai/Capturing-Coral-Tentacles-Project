from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import string

from Image import *
from InstructionsWindow import InstructionsWindow

def generalTabUI(self):

        generalTab = QWidget()
        self.generalLayout = QGridLayout()

        self.photo = Image()

        self.generalLayout.addWidget(self.photo, 0, 0)

        self.g = None
        self.w = None
        
        self.instructionsButton = QPushButton("Instructions")
        self.instructionsButton.clicked.connect(self.instruct)
        
        self.savePicButton = QPushButton("Save Picture to Record")
        self.savePicButton.clicked.connect(self.recordInfo)
        
        self.countButton = QPushButton("Count")
        self.countButton.clicked.connect(self.countTentacles)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count())))

        self.removeMarkerButton = QPushButton('Remove Marker')
        self.removeMarkerButton.clicked.connect(self.photo.remove_marker)
        self.removeMarkerButton.clicked.connect(self.updateMarkerCount)

        self.undoMarkerButton = QPushButton('Undo Last Marker')
        self.undoMarkerButton.clicked.connect(self.photo.undo_last_marker)
        self.undoMarkerButton.clicked.connect(self.updateMarkerCount)

        self.changeColorButton = QToolButton()
        self.changeColorButton.setText("Change Color")
        self.color_menu = QMenu()
        self.changeColorButton.setMenu(self.color_menu)

        # Add different color options to the drop-down menu
        self.colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Black", "White"]
        for color in self.colors:
            action = QAction(color, self)
            action.triggered.connect(lambda _, color=color: self.photo.change_color(color))
            self.color_menu.addAction(action)

        self.changeColorButton.clicked.connect(self.color_menu.show)

        self.color_menu.clear()
        colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Black", "White"]
        for color in colors:
            action = QAction(color, self)
            action.triggered.connect(lambda _, color=color: self.photo.change_color(color))
            self.color_menu.addAction(action)

        self.photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.photo.view.setRenderHint(QPainter.Antialiasing)
        self.photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.zoomInButton = QPushButton('Zoom In')
        self.zoomOutButton = QPushButton('Zoom Out')
        self.zoomInButton.clicked.connect(self.photo.zoom_in)
        self.zoomOutButton.clicked.connect(self.photo.zoom_out)

        self.setMouseTracking(True)

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
        self.smallerGridLayout.addWidget(self.countDisplay, 0, 1)
        
        self.smallGridLayout = QGridLayout()
        self.smallGridLayout.addWidget(self.instructionsButton, 0, 0)
        self.smallGridLayout.addWidget(self.savePicButton, 1, 0)
        self.smallGridLayout.addWidget(self.countButton, 2, 0)
        self.smallGridLayout.addLayout(self.smallerGridLayout, 3, 0)
        self.smallGridLayout.addWidget(self.removeMarkerButton, 4, 0)
        self.smallGridLayout.addWidget(self.undoMarkerButton, 5, 0)
        self.smallGridLayout.addWidget(self.changeColorButton, 6, 0)

        self.smallGridLayout.addWidget(self.zoomInButton, 7, 0)
        self.smallGridLayout.addWidget(self.zoomOutButton, 8, 0)

        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        
        # Stylesheets
        self.countLabel.setStyleSheet(
            "color: #112d4e;"
        )
        
        self.savePicButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        self.countButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        self.removeMarkerButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
        )
        self.undoMarkerButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;" 
        )
        
        self.instructionsButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;"
            "background-color : #00adb5;"
        )

        self.changeColorButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;" 
        )

        self.zoomInButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;" 
        )

        self.zoomOutButton.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;" 
        )

        self.setStyleSheet(
            "QLabel {color: blue;}"
        )

        generalTab.setLayout(self.generalLayout)
        return generalTab
    
    