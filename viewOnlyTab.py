"""A version of the generalTab with no functionality.
Used when opening someone else's image; the user should only
be able to view the image, not edit it."""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *

def viewOnlyTabUI(self, load_image, load_count, load_coordinates, owner_name, owner_notes):
    viewOnlyTab = QWidget()
    self.generalLayout = QGridLayout()

    self.loadImageName = load_image
    self.tentacleCount = load_count
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
    self.view_photo.zoom_in()

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

    self.view_countLabel = QLabel("Tentacle Count:")
    self.view_countDisplay = QLineEdit("{0}".format(self.tentacleCount))
    self.view_countDisplay.setReadOnly(True)
    self.view_countGridLayout = QGridLayout()
    self.view_countGridLayout.addWidget(self.view_countLabel, 0, 0)
    self.view_countGridLayout.addWidget(self.view_countDisplay, 0, 1)

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

    self.zoomin_shortcut = QShortcut(QKeySequence("Ctrl+="), self)
    self.zoomout_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
    self.zoomin_shortcut.activated.connect(self.view_photo.zoom_in)
    self.zoomout_shortcut.activated.connect(self.view_photo.zoom_out)

    self.rightGridLayout = QGridLayout()
    self.rightGridLayout.addLayout(self.view_photo.fileGridLayout, 1, 0)
    self.rightGridLayout.addLayout(self.view_photo.ownerGridLayout, 2, 0)
    self.rightGridLayout.addLayout(self.view_countGridLayout, 3, 0)
    self.rightGridLayout.addLayout(self.notesGridLayout, 4, 0)
    self.rightGridLayout.addLayout(self.smallGridLayout, 5, 0)

    self.generalLayout.addLayout(self.rightGridLayout, 0, 1)

    
    # Stylesheets
    self.zoomInButton.setStyleSheet(
        " color: white;"
        " background-color: #3f72af;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        " border-radius: 10px;"
        " padding: 10px 20px;"
    )

    self.zoomOutButton.setStyleSheet(
        " color: white;"
        " background-color: #3f72af;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        " border-radius: 10px;"
        " padding: 10px 20px;"
    )

    self.setStyleSheet(
        "QLabel {color: white;}"
    )

    self.view_countDisplay.setStyleSheet(
        "border: none;"
    )
    self.notesDisplay.setStyleSheet(
        "border: none;"
    )

    self.setStyleSheet(
        "QLabel {"
        " color: #00adb5;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        "}"

        "QPushButton {"
        " color: white;"
        " background-color: #3f72af;"
        " font-family: 'Lucida Sans Typewriter';"
        " font-size: 15px;"
        " font-weight: bold;"
        " border-radius: 10px;"
        " padding: 10px 20px;"
        "}"

        "QPushButton:hover {"
        " background-color: #00adb5;"
        "}"

        "QLineEdit {"
        " font-size: 15px;"
        " font-family: 'Lucida Sans Typewriter';"
        "}"

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
                point_x /= 1.3

            coralImage.add_marker(point_x, point_y, color)