from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PhotoLabel import *
from main import SplashScreen

import platform
import os.path
import PIL

class CoralImage(QWidget):
    
    clicked = pyqtSignal()
    openedImage = pyqtSignal()
    
    def __init__(self, isViewOnly):
        super().__init__()
        self.photo = PhotoLabel()
        self.photo.setFixedWidth(800)
        self.photo.setFixedHeight(500)
        
        self.browse_btn = QPushButton('Browse')
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setFixedWidth(800)
        self.browse_btn.setFixedHeight(50)
        
        self.browse_btn.setStyleSheet(
            "color: white;"
            "background-color: #00adb5;"
        )
        
        self.pix = QPixmap()
        self.browse_btn.clicked.connect(self.open_image)
        self.browse_btn.clicked.connect(self.openedImage.emit)
        
        self.path = ""
        self.file = ""
        self.isViewOnly = isViewOnly

        self.photo_grid = QGridLayout(self)

        if not isViewOnly:
            self.photo_grid.addWidget(self.browse_btn, 0, 0, Qt.AlignTop)

        self.photo_grid.addWidget(self.photo, 1, 0)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        
        self.view.setStyleSheet(
            "background: transparent;"
        )
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.photo_grid.addWidget(self.view, 1, 0)

        # Set up loading image but hide it
        if platform.system() == "Windows":
            self.loading_image = os.getcwd() + "\style_images\loading_image.png"
        else:
            self.loading_image = os.getcwd() + "/style_images/loading_image.png"
        self.loading_pixmap = QPixmap(self.loading_image)
        self.loading_scene = QGraphicsScene()
        self.loading_scene.addPixmap(self.loading_pixmap)
        self.loading_view = QGraphicsView(self.loading_scene)
        self.loading_view.setFixedSize(800, 500)

        self.loading_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.loading_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.photo_grid.addWidget(self.loading_view, 1, 0)
        self.loading_view.hide()

        self.marker_count = 0
        self.markers = []
        self.marker_colors = []
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.fileGridLayout = QGridLayout()
        self.filenameLabel = QLabel("Current image being displayed:")
        if isViewOnly:
            self.filenameLabel.setText("Image Name:")
        self.filenameDisplay = QLineEdit("{0}".format(self.get_filename()))
        self.filenameDisplay.setReadOnly(True)
        self.fileGridLayout.addWidget(self.filenameLabel, 0, 0)
        self.fileGridLayout.addWidget(self.filenameDisplay, 0, 1)
        
        if not isViewOnly:
            self.photo_grid.addLayout(self.fileGridLayout, 2, 0)

        self.modelGridLayout = QGridLayout()
        self.modelLabel = QLabel("Model Status:")
        self.modelDisplay = QLineEdit("Inactive")
        self.modelDisplay.setReadOnly(True)
        self.modelGridLayout.addWidget(self.modelLabel, 0, 0)
        self.modelGridLayout.addWidget(self.modelDisplay, 0, 1)

        if not isViewOnly:
            self.photo_grid.addLayout(self.modelGridLayout, 3, 0)

        self.ownerGridLayout = QGridLayout()
        self.imageOwnerLabel = QLabel("Image Owner:")
        self.imageOwnerDisplay = QLineEdit("{0}".format("-"))
        self.imageOwnerDisplay.setReadOnly(True)
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
        
        self.colorChange.setCurrentIndex(2)
        self.colorChange.activated[str].connect(self.change_color)
        
        # Keyboard shortcuts
        self.browse_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.browse_shortcut.activated.connect(self.open_image)
        self.browse_shortcut.activated.connect(self.openedImage.emit)

        self.filenameDisplay.setStyleSheet(
            "border: none;"
        )        
        self.imageOwnerDisplay.setStyleSheet(
            "border: none;"
        )
        self.modelDisplay.setStyleSheet(
            "border: none;"
        )

    def open_image(self, filename=None):
        self.marker_count = 0
        self.markers.clear()

        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return "Image not found"
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
        self.browse_btn.setFixedWidth(self.view.width())
        self.scene.clear()
        self.scene.addPixmap(self.smaller_pixmap)
        self.filenameDisplay.setText("{0}".format(self.get_filename()))

    def set_loading_image(self):
        self.photo.hide()
        self.view.hide()
        self.loading_view.show()

    def hide_loading_image(self):
        self.loading_view.hide()
        self.photo.show()
        self.view.show()
        
    def get_filename(self):
        return self.file
    
    def get_path(self):
        return self.path
    
    def get_marker_count(self):
        return self.marker_count
         
    def get_markersList(self):
        return self.markers
         
    def add_marker(self, x_pos, y_pos, color_name):
        if self.file is not "":
            ellipse = QGraphicsEllipseItem(0, 0, 15, 15)
            ellipse.setBrush(QBrush(self.color_dict[color_name]))
            
            if not self.isViewOnly:
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
        marker_list_length = len(self.markers)
        if marker_list_length > 0 and not self.isViewOnly:
            reversed_markers = list(reversed(self.markers))
            reversed_colors = list(reversed(self.marker_colors))

            for i, marker in enumerate(reversed_markers):
                if reversed_colors[i] != "YOLO Red":
                    index = self.markers.index(marker)
                    self.scene.removeItem(marker)
                    self.markers.pop(index)
                    self.marker_colors.pop(index)
                    self.marker_count -= 1

                    return

    def zoom_in(self):
        self.view.scale(1.2, 1.2)

    def zoom_out(self):
        self.view.scale(1/1.2, 1/1.2)
        
    def change_color(self, color):
        brush_color = self.color_dict[color]        
        for marker in self.markers:
            if marker.isSelected():
                marker.setBrush(QBrush(brush_color))
                i = self.markers.index(marker)
                self.marker_colors[i] = color

    def mousePressEvent(self, QMouseEvent):
        if (self.file is not "" and QMouseEvent.type() == QEvent.MouseButtonDblClick
        and not self.isViewOnly):
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.add_marker(x-19, y-81, self.colorChange.currentText())
            self.clicked.emit()


    