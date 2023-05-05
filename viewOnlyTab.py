"""A version of the generalTab with no functionality.
Used when opening someone else's image; the user should only
be able to view the image, not edit it."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Image import *

def viewOnlyTabUI(self):
    # id = QFontDatabase.addApplicationFont("fonts/Montserrat/Montserrat-Regular.ttf")
    # families = QFontDatabase.applicationFontFamilies(id)
    # montserrat_font = families[0]

    viewOnlyTab = QWidget()
    self.generalLayout = QGridLayout()

    self.photo = Image()
    self.photo.browse_btn.setEnabled(False)
    self.photo.browse_shortcut.activated.disconnect()

    self.generalLayout.addWidget(self.photo, 0, 0)

    self.g = None
    self.w = None
    
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

    self.smallGridLayout = QGridLayout()
    self.smallGridLayout.addWidget(self.zoomInButton, 0, 0)
    self.smallGridLayout.addWidget(self.zoomOutButton, 1, 0)

    self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

    
    # Stylesheets
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

    viewOnlyTab.setLayout(self.generalLayout)
    return viewOnlyTab
