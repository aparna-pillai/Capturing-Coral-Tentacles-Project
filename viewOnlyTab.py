"""A version of the generalTab with no functionality.
Used when opening someone else's image; the user should only
be able to view the image, not edit it."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *

def viewOnlyTabUI(self, load_image, load_coordinates, owner_name):
    # id = QFontDatabase.addApplicationFont("fonts/Montserrat/Montserrat-Regular.ttf")
    # families = QFontDatabase.applicationFontFamilies(id)
    # montserrat_font = families[0]

    viewOnlyTab = QWidget()
    self.generalLayout = QGridLayout()

    self.loadImageName = load_image
    self.ownerName = owner_name
    self.coordString = load_coordinates
    self.coordList = load_coordinates.split("|")

    self.view_photo = CoralImage(isViewOnly=True)
    self.view_photo.browse_btn.setEnabled(False)

    self.view_photo.open_image(filename=self.loadImageName)
    self.view_photo.imageOwnerDisplay.setText("{0}".format(self.ownerName))

    placeLoadedCoordinates(self.coordList, self.view_photo)

    # for point in self.coordList:
    #     color = point.split(";")[1].strip()
    #     coord = point.split(";")[0].strip()
    #     point_x = float(coord.split(",")[0].strip())
    #     point_y = float(coord.split(",")[1].strip())

    #     self.view_photo.add_marker(point_x, point_y, color)

    self.generalLayout.addWidget(self.view_photo, 0, 0)

    self.view_photo.view.setFixedWidth(800)
    self.view_photo.view.setFixedHeight(500)
    
    self.view_photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
    self.view_photo.view.setRenderHint(QPainter.Antialiasing)
    self.view_photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
    self.view_photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.view_photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    self.view_photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.closeTabButton = QPushButton('Close Tab')
    self.closeTabButton.clicked.connect(self.closeViewOnlyTab)

    self.zoomInButton = QPushButton('Zoom In')
    self.zoomOutButton = QPushButton('Zoom Out')
    # self.zoomInButton.setFont(QFont(montserrat_font))
    # self.zoomOutButton.setFont(QFont(montserrat_font))
    self.zoomInButton.clicked.connect(self.view_photo.zoom_in)
    self.zoomOutButton.clicked.connect(self.view_photo.zoom_out)

    self.setMouseTracking(True)

    self.smallGridLayout = QGridLayout()
    self.smallGridLayout.addWidget(self.zoomInButton, 0, 0)
    self.smallGridLayout.addWidget(self.zoomOutButton, 0, 1)

    self.allButtonsGridLayout = QGridLayout()
    self.allButtonsGridLayout.addWidget(self.closeTabButton, 0, 0)
    self.allButtonsGridLayout.addLayout(self.smallGridLayout, 1, 0)

    self.generalLayout.addLayout(self.allButtonsGridLayout, 0, 1)

    
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
        "width: 250px;"
    )

    self.setStyleSheet(
        "QLabel {color: blue;}"
    )

    viewOnlyTab.setLayout(self.generalLayout)
    return viewOnlyTab


def placeLoadedCoordinates(coordList, coralImage):
    print(coordList)
    if coordList[0] == '':
        return
    else:
        for point in coordList:
            color = point.split(";")[1].strip()
            coord = point.split(";")[0].strip()
            point_x = float(coord.split(",")[0].strip())
            point_y = float(coord.split(",")[1].strip())

            coralImage.add_marker(point_x, point_y, color)