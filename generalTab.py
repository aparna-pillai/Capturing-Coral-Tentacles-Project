from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *

def generalTabUI(self):
    generalTab = QWidget()
    self.generalLayout = QGridLayout()

    # palette = self.palette()
    # palette.setBrush(QPalette.Window, QColor(94, 37, 204))  
    # self.setPalette(palette)

    self.modelHasCounted = False

    self.photo = CoralImage(isViewOnly=False)
    self.photo.view.setFixedWidth(800)
    self.photo.view.setFixedHeight(500)

    self.generalLayout.addWidget(self.photo, 0, 0)
    self.photo.clicked.connect(self.updateMarkerCount)

    self.photo.browse_btn.clicked.connect(self.clearOldCoordinates)
    self.photo.browse_shortcut.activated.connect(self.clearOldCoordinates)

    self.g = None
    self.w = None
    
    self.instructionsButton = QPushButton("Instructions")
    # self.instructionsButton.setFont(QFont(montserrat_font))
    self.instructionsButton.clicked.connect(self.instruct)
    self.instructionsButton.setFixedSize(300, 40)

    self.savePicButton = QPushButton("Save Picture to Record")
    # self.savePicButton.setFont(QFont(montserrat_font))
    self.savePicButton.clicked.connect(self.recordInfo)
    self.savePicButton.setFixedSize(300, 40)
    
    self.countButton = QPushButton("Count")
    self.countButton.clicked.connect(self.countTentacles)
    self.countButton.setFixedSize(300, 40)
    # self.countButton.setFont(QFont(montserrat_font))
    
    self.countLabel = QLabel("Tentacle Count:")
    # self.countLabel.setFont(QFont(montserrat_font))
    
    self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count())))
    # self.countDisplay.setFont(QFont(montserrat_font))

    self.removeMarkerButton = QPushButton('Remove Marker')
    # self.removeMarkerButton.setFont(QFont(montserrat_font))
    self.removeMarkerButton.clicked.connect(self.photo.remove_marker)
    self.removeMarkerButton.clicked.connect(self.updateMarkerCount)
    self.removeMarkerButton.setFixedSize(300, 40)

    self.undoMarkerButton = QPushButton('Undo Last Marker')
    # self.undoMarkerButton.setFont(QFont(montserrat_font))
    self.undoMarkerButton.clicked.connect(self.photo.undo_last_marker)
    self.undoMarkerButton.clicked.connect(self.updateMarkerCount)
    self.undoMarkerButton.setFixedSize(300, 40)

    self.clearAllMarkersButton = QPushButton('Delete All Markers')
    self.clearAllMarkersButton.clicked.connect(self.confirmForClearCoordinates)
    self.clearAllMarkersButton.setFixedSize(300, 40)

    self.photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
    self.photo.view.setRenderHint(QPainter.Antialiasing)
    self.photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
    self.photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    self.photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.zoomInButton = QPushButton('Zoom In')
    self.zoomInButton.setFixedSize(300, 40)

    self.zoomOutButton = QPushButton('Zoom Out')
    self.zoomOutButton.setFixedSize(300, 40)
    # self.zoomInButton.setFont(QFont(montserrat_font))
    # self.zoomOutButton.setFont(QFont(montserrat_font))
    self.zoomInButton.clicked.connect(self.photo.zoom_in)
    self.zoomOutButton.clicked.connect(self.photo.zoom_out)

    self.setMouseTracking(True)

    self.smallerGridLayout = QGridLayout()
    self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
    self.smallerGridLayout.addWidget(self.countDisplay, 1, 0)
    self.countDisplay.setFixedSize(300, 40)
    
    self.smallGridLayout = QGridLayout()
    self.smallGridLayout.addWidget(self.instructionsButton, 0, 0)
    self.smallGridLayout.addWidget(self.savePicButton, 1, 0)
    self.smallGridLayout.addWidget(self.countButton, 2, 0)
    self.smallGridLayout.addLayout(self.smallerGridLayout, 3, 0)
    self.smallGridLayout.addWidget(self.removeMarkerButton, 4, 0)
    self.smallGridLayout.addWidget(self.clearAllMarkersButton, 5, 0)
    self.smallGridLayout.addWidget(self.undoMarkerButton, 6, 0)
    self.smallGridLayout.addWidget(self.zoomInButton, 7, 0)
    self.smallGridLayout.addWidget(self.zoomOutButton, 8, 0)
    
    # self.smallestGridLayout = QGridLayout()
    self.smallerGridLayout.addWidget(self.photo.colorChange_Label, 9, 0)
    self.smallerGridLayout.addWidget(self.photo.colorChange, 10, 0)
    self.photo.colorChange.setFixedSize(300, 40)
    #self.smallGridLayout.addWidget(self.photo.color_menu, 9, 0)
    
    self.generalLayout.addLayout(self.smallGridLayout, 0, 1)
    # self.generalLayout.addLayout(self.smallestGridLayout, 1, 1)
    
    # Stylesheets
    self.countLabel.setStyleSheet(
        "color: #112d4e;"
    )
    
    self.photo.colorChange_Label.setStyleSheet(
        "color: #112d4e;"
    )
    
    # self.savePicButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    # )
    # self.countButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    # )
    # self.clearAllMarkersButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    # )
    # self.removeMarkerButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    # )
    # self.undoMarkerButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;" 
    # )
    
    # self.instructionsButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;"
    #     "background-color : #00adb5;"
    # )

    self.photo.colorChange.setStyleSheet(
        "border: 3px solid;"
        "border-top-color: #f30497;"
        "border-left-color: #f30497;"
        "border-right-color: #f30497;"
        "border-bottom-color: #f30497;"
        "color: #112d4e;" 
        "padding-right: 8px;"
        "width: 250px;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 13px;"
        
    )

    # self.zoomInButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;" 
    # )

    # self.zoomOutButton.setStyleSheet(
    #     "border: 3px solid;"
    #     "border-top-color: #00adb5;"
    #     "border-left-color: #00adb5;"
    #     "border-right-color: #00adb5;"
    #     "border-bottom-color: #00adb5;"
    #     "color: #112d4e;" 
    # )

    self.setStyleSheet(
        "QLabel {"
        " color: #f30497;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        "}"

        "QPushButton {"
        " color: white;"
        " background-color: #4216a1;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        " border-radius: 10px;"
        " padding: 10px 20px;"
        "}"

        "QPushButton:hover {"
        " background-color: #f30497;"
        "}"

        "QLineEdit {"
        " font-size: 15px;"
        " font-family: 'Lucida Sans Typewriter';"
        "}"

    )

    generalTab.setLayout(self.generalLayout)
    return generalTab
