from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PhotoLabel import *

import platform
import os.path

class CoralImage(QWidget):
    
    def __init__(self, isViewOnly):
        super().__init__()
        self.photo = PhotoLabel()
        self.photo.setFixedWidth(800)
        self.photo.setFixedHeight(500)
        
        self.browse_btn = QPushButton('Browse')
        self.browse_btn.setFixedWidth(800)
        self.browse_btn.setFixedHeight(50)
        
        self.browse_btn.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #3f72af;"
            "border-left-color: #3f72af;"
            "border-right-color: #3f72af;"
            "border-bottom-color: #3f72af;"
            "color: #00adb5;"
        )
        
        self.pix = QPixmap()
        self.browse_btn.clicked.connect(self.open_image)
        
        self.path = ""
        self.file = ""
        
        grid = QGridLayout(self)

        if not isViewOnly:
            grid.addWidget(self.browse_btn, 0, 0, Qt.AlignTop)

        grid.addWidget(self.photo, 1, 0)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        
        self.view.setStyleSheet(
            "background: transparent;"
        )
        grid.addWidget(self.view, 1, 0, 1, 0)

        self.marker_count = 0
        self.markers = []
        self.marker_colors = []
        self.setAcceptDrops(True)

        self.fileGridLayout = QGridLayout()
        self.filenameLabel = QLabel("Current image being displayed:")
        self.filenameDisplay = QLineEdit("{0}".format(self.get_filename()))
        self.fileGridLayout.addWidget(self.filenameLabel, 0, 0)
        self.fileGridLayout.addWidget(self.filenameDisplay, 0, 1)
        
        if not isViewOnly:
            grid.addLayout(self.fileGridLayout, 2, 0)

        self.ownerGridLayout = QGridLayout()
        self.imageOwnerLabel = QLabel("Image owner:")
        self.imageOwnerDisplay = QLineEdit("{0}".format(324324))
        self.ownerGridLayout.addWidget(self.imageOwnerLabel, 0, 0)
        self.ownerGridLayout.addWidget(self.imageOwnerDisplay, 0, 1)

        self.selected_marker = None 

        self.color_dict = {
            "YOLO Red": QColor(245, 96, 42), "Red": Qt.red, "Orange": QColor(255, 137, 0), 
            "Yellow": Qt.yellow, "Green": Qt.green, "Blue": Qt.blue, 
            "Purple": QColor(219, 0, 255), "Pink": QColor(245, 66, 164), "Black": Qt.black, 
            "White": Qt.white
        }
        
        self.colorChange_Label = QLabel("Change Color of Selected Marker: ")
        self.colorChange = QComboBox()
        for key in self.color_dict:
            if key != "YOLO Red":
                self.colorChange.addItem(key)
        
        self.colorChange.activated[str].connect(self.change_color)
        
        # Keyboard shortcuts
        self.browse_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.browse_shortcut.activated.connect(self.open_image)

        self.filenameDisplay.setStyleSheet(
            "border: none;"
        )        
        self.imageOwnerDisplay.setStyleSheet(
            "border: none;"
        )

    def open_image(self, filename=None):
        self.marker_count = 0
        self.markers.clear()

        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            self.path = str(filename)
            self.file = QFileInfo(filename).fileName()
        else:
            if platform.system() == 'Windows':
                self.path = os.getcwd() + '\\' + filename
            else:
                self.path = os.getcwd() + '/' + filename
            self.file = filename
            
        self.photo.setStyleSheet(
            "background: transparent;"
        )
        self.pix = QPixmap(filename)
        self.smaller_pixmap = self.pix.scaled(self.view.width(), self.view.height())
        self.scene.clear()
        self.scene.addPixmap(self.smaller_pixmap)
        self.filenameDisplay.setText("{0}".format(self.get_filename()))
        
        
        
    def get_filename(self):
        return self.file
    
    def get_path(self):
        return self.path
    
    def get_marker_count(self):
        return self.marker_count
         
    def get_markersList(self):
        return self.markers
         
    def add_marker(self, x_pos, y_pos, color_name, isViewOnly):
        if self.file is not "":
            ellipse = QGraphicsEllipseItem(0, 0, 15, 15)
            ellipse.setBrush(QBrush(self.color_dict[color_name]))
            
            if not isViewOnly:
                ellipse.setFlag(QGraphicsItem.ItemIsMovable)
                ellipse.setFlag(QGraphicsItem.ItemIsSelectable)
            
            ellipse.setPos(x_pos, y_pos)

            self.scene.addItem(ellipse)
            self.marker_count += 1
            self.markers.append(ellipse)
            self.marker_colors.append(color_name)

    def set_selected_marker(self, marker):
        self.selected_marker = marker

    def remove_marker(self):
        for i, marker in enumerate(self.markers):
            if marker.isSelected():
                self.scene.removeItem(marker)
                self.markers.pop(i)
                self.marker_colors.pop(i)
                self.marker_count -= 1

    def undo_last_marker(self):
        if len(self.markers) > 0:
            last_marker = self.markers[len(self.markers) - 1]
            self.scene.removeItem(last_marker)
            self.markers.pop(len(self.markers) - 1)
            self.marker_colors.pop(len(self.markers) - 1)
            self.marker_count -= 1

    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    def zoom_out(self):
        self.view.scale(1/1.2, 1/1.2)
        
    def change_color(self, color):
        brush_color = self.color_dict[color]        
        for marker in self.markers:
            if marker.isSelected():
                marker.setBrush(QBrush(brush_color))



    