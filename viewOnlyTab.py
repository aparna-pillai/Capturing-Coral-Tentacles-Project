"""A version of the generalTab with no functionality.
Used when opening someone else's image; the user should only
be able to view the image, not edit it."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Image import *

def viewOnlyTabUI(self, load_image, load_coordinates):
    # id = QFontDatabase.addApplicationFont("fonts/Montserrat/Montserrat-Regular.ttf")
    # families = QFontDatabase.applicationFontFamilies(id)
    # montserrat_font = families[0]

    viewOnlyTab = QWidget()
    self.generalLayout = QGridLayout()

    self.loadImage = load_image
    self.coordString = load_coordinates
    self.coordList = load_coordinates.split("|")

    self.view_photo = Image()
    self.view_photo.browse_btn.setEnabled(False)
    self.view_photo.browse_shortcut.activated.disconnect()

    # self.view_photo.open_image(self.loadImage)
    # Currently doesn't work since an image name ("IMG-6268.JPG") is not an actual filename

    self.generalLayout.addWidget(self.view_photo, 0, 0)

    self.view_photo.view.setFixedWidth(800)
    self.view_photo.view.setFixedHeight(500)

    self.g = None
    self.w = None
    
    self.view_photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
    self.view_photo.view.setRenderHint(QPainter.Antialiasing)
    self.view_photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
    self.view_photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.view_photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    self.view_photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.zoomInButton = QPushButton('Zoom In')
    self.zoomOutButton = QPushButton('Zoom Out')
    # self.zoomInButton.setFont(QFont(montserrat_font))
    # self.zoomOutButton.setFont(QFont(montserrat_font))
    self.zoomInButton.clicked.connect(self.view_photo.zoom_in)
    self.zoomOutButton.clicked.connect(self.view_photo.zoom_out)

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
        "width: 250px;" 
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
