"""A version of the generalTab with no functionality.
Used when opening someone else's image; the user should only
be able to view the image, not edit it."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *

def viewOnlyTabUI(self, load_image, load_coordinates, owner_name, owner_notes):
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

    self.view_photo.marker_count = 0
    self.updateMarkerCount()
    self.view_photo.markers.clear()
    self.coordinate_list.clear()

    self.view_photo.open_image(filename=self.loadImageName)
    self.view_photo.imageOwnerDisplay.setText("{0}".format(self.ownerName))

    placeLoadedCoordinates(self.coordList, self.view_photo, True)

    self.generalLayout.addWidget(self.view_photo, 0, 0)

    self.view_photo.view.setFixedWidth(800)
    self.view_photo.view.setFixedHeight(500)
    
    self.view_photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
    self.view_photo.view.setRenderHint(QPainter.Antialiasing)
    self.view_photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
    self.view_photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    self.view_photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    self.view_photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    self.countLabel = QLabel("Tentacle Count:")
    self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count())))
    self.countDisplay.setReadOnly(True)
    self.countGridLayout = QGridLayout()
    self.countGridLayout.addWidget(self.countLabel, 0, 0)
    self.countGridLayout.addWidget(self.countDisplay, 0, 1)

    self.notesLabel = QLabel("Notes:")
    self.notesDisplay = QLineEdit(owner_notes)
    self.notesDisplay.setReadOnly(True)
    self.notesGridLayout = QGridLayout()
    self.notesGridLayout.addWidget(self.notesLabel, 0, 0)
    self.notesGridLayout.addWidget(self.notesDisplay, 0, 1)

    self.zoomInButton = QPushButton('Zoom In')
    self.zoomOutButton = QPushButton('Zoom Out')
    self.zoomInButton.clicked.connect(self.view_photo.zoom_in)
    self.zoomOutButton.clicked.connect(self.view_photo.zoom_out)

    self.setMouseTracking(True)

    self.smallGridLayout = QGridLayout()
    self.smallGridLayout.addWidget(self.zoomInButton, 0, 0)
    self.smallGridLayout.addWidget(self.zoomOutButton, 0, 1)

    self.rightGridLayout = QGridLayout()
    self.rightGridLayout.addLayout(self.view_photo.fileGridLayout, 1, 0)
    self.rightGridLayout.addLayout(self.view_photo.ownerGridLayout, 2, 0)
    self.rightGridLayout.addLayout(self.countGridLayout, 3, 0)
    self.rightGridLayout.addLayout(self.notesGridLayout, 4, 0)
    self.rightGridLayout.addLayout(self.smallGridLayout, 5, 0)

    self.generalLayout.addLayout(self.rightGridLayout, 0, 1)

    
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

    self.countDisplay.setStyleSheet(
        "border: none;"
    )
    self.notesDisplay.setStyleSheet(
        "border: none;"
    )

    viewOnlyTab.setLayout(self.generalLayout)
    return viewOnlyTab


def placeLoadedCoordinates(coordList, coralImage, isViewOnly):
    if coordList[0] == '':
        return
    else:
        for point in coordList:
            color = point.split(";")[1].strip()
            coord = point.split(";")[0].strip()
            
            point_x = float(coord.split(",")[0].strip())
            point_y = float(coord.split(",")[1].strip())
            if isViewOnly:
                point_x -= 100

            coralImage.add_marker(point_x, point_y, color, isViewOnly)