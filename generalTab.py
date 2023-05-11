from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *

def generalTabUI(self):
    generalTab = QWidget()
    self.generalLayout = QGridLayout()

    self.modelHasCounted = False

    self.photo = CoralImage(isViewOnly=False)
    self.photo.view.setFixedWidth(800)
    self.photo.view.setFixedHeight(500)

    self.generalLayout.addWidget(self.photo, 0, 0)

    self.photo.browse_btn.clicked.connect(self.clearOldCoordinates)
    self.photo.browse_shortcut.activated.connect(self.clearOldCoordinates)

    self.g = None
    self.w = None
    
    self.instructionsButton = QPushButton("Instructions")
    # self.instructionsButton.setFont(QFont(montserrat_font))
    self.instructionsButton.clicked.connect(self.instruct)
    
    self.savePicButton = QPushButton("Save Picture to Record")
    # self.savePicButton.setFont(QFont(montserrat_font))
    self.savePicButton.clicked.connect(self.recordInfo)
    
    self.countButton = QPushButton("Count")
    # self.countButton.setFont(QFont(montserrat_font))
    if self.modelHasCounted == False:
        self.countButton.clicked.connect(self.countTentacles)
        self.countButton.clicked.connect(self.setModelCountedTrue)
    
    self.countLabel = QLabel("Tentacle Count:")
    # self.countLabel.setFont(QFont(montserrat_font))
    
    self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count())))
    # self.countDisplay.setFont(QFont(montserrat_font))

    self.removeMarkerButton = QPushButton('Remove Marker')
    # self.removeMarkerButton.setFont(QFont(montserrat_font))
    self.removeMarkerButton.clicked.connect(self.photo.remove_marker)
    self.removeMarkerButton.clicked.connect(self.updateMarkerCount)

    self.undoMarkerButton = QPushButton('Undo Last Marker')
    # self.undoMarkerButton.setFont(QFont(montserrat_font))
    self.undoMarkerButton.clicked.connect(self.photo.undo_last_marker)
    self.undoMarkerButton.clicked.connect(self.updateMarkerCount)

    self.photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
    self.photo.view.setRenderHint(QPainter.Antialiasing)
    self.photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
    self.photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    self.photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.zoomInButton = QPushButton('Zoom In')
    self.zoomOutButton = QPushButton('Zoom Out')
    # self.zoomInButton.setFont(QFont(montserrat_font))
    # self.zoomOutButton.setFont(QFont(montserrat_font))
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
    self.smallGridLayout.addWidget(self.zoomInButton, 6, 0)
    self.smallGridLayout.addWidget(self.zoomOutButton, 7, 0)
    
    self.smallestGridLayout = QGridLayout()
    self.smallestGridLayout.addWidget(self.photo.colorChange_Label, 0, 0)
    self.smallestGridLayout.addWidget(self.photo.colorChange, 0, 1)
    #self.smallGridLayout.addWidget(self.photo.color_menu, 9, 0)
    
    self.generalLayout.addLayout(self.smallGridLayout, 0, 1)
    self.generalLayout.addLayout(self.smallestGridLayout, 1, 1)
    
    # Stylesheets
    self.countLabel.setStyleSheet(
        "color: #112d4e;"
    )
    
    self.photo.colorChange_Label.setStyleSheet(
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

    self.photo.colorChange.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #00adb5;"
        "border-left-color: #00adb5;"
        "border-right-color: #00adb5;"
        "border-bottom-color: #00adb5;"
        "color: #112d4e;" 
        "padding-right: 8px;"
        "width: 250px;"
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
