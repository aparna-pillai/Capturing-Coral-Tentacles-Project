from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from CoralImage import *
from InstructionsWindow import *
from RecordInfoWindow import *
from viewOnlyTab import *

from coral_count import *
from connectToDatabase import *
from basic_styling import *

from threading import Thread

class GeneralTab(QWidget):

    placeMarkersCall = pyqtSignal()
    showLoadingImage = pyqtSignal()
    hideLoadingImage = pyqtSignal()
    generalDbConnectCalled = pyqtSignal(QTableWidget)

    def __init__(self, tabWidget, username, tableWidget):
        super().__init__()
        self.generalLayout = QGridLayout()
        self.setLayout(self.generalLayout)

        self.general_tabs = tabWidget
        self.general_username = username
        self.general_tables = tableWidget

        self.coordinate_list = []

        self.photo = CoralImage(isViewOnly=False)
        self.photo.view.setFixedWidth(800)
        self.photo.view.setFixedHeight(500)
        self.generalLayout.addWidget(self.photo, 0, 0)

        # Signal and slot connections
        self.photo.clicked.connect(self.updateMarkerCount)
        self.photo.openedImage.connect(lambda: self.photo.modelDisplay.setText("Inactive"))
        self.showLoadingImage.connect(self.photo.set_loading_image)
        self.hideLoadingImage.connect(self.photo.hide_loading_image)

        self.placeMarkersCall.connect(self.placeInitialMarkers)

        self.photo.browse_btn.clicked.connect(self.clearOldCoordinates)
        self.photo.browse_shortcut.activated.connect(self.clearOldCoordinates)

        self.g = None
        self.w = None
        
        self.instructionsButton = QPushButton("Instructions")
        self.instructionsButton.setCursor(Qt.PointingHandCursor)
        self.instructionsButton.clicked.connect(self.instruct)
        self.instructionsButton.setFixedSize(400, 40)

        self.savePicButton = QPushButton("Save Picture to Record")
        self.savePicButton.setCursor(Qt.PointingHandCursor)
        self.savePicButton.clicked.connect(self.recordInfo)
        self.savePicButton.setFixedSize(400, 40)
        
        self.countButton = QPushButton("Count")
        self.countButton.setCursor(Qt.PointingHandCursor)
        self.countButton.clicked.connect(self.modelStart)
        self.countButton.setFixedSize(400, 40)
        
        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count())))
        self.countDisplay.setReadOnly(True)

        self.removeMarkerButton = QPushButton('Remove Marker')
        self.removeMarkerButton.setCursor(Qt.PointingHandCursor)
        self.removeMarkerButton.setToolTip("Make sure a marker is selected.")
        self.removeMarkerButton.clicked.connect(self.photo.remove_marker)
        self.removeMarkerButton.clicked.connect(self.updateMarkerCount)
        self.removeMarkerButton.setFixedSize(400, 40)

        self.undoMarkerButton = QPushButton('Undo Last Marker')
        self.undoMarkerButton.setCursor(Qt.PointingHandCursor)
        self.undoMarkerButton.setToolTip(
            "Only markers that you have placed will be undone, not the model's."
        )
        self.undoMarkerButton.clicked.connect(self.photo.undo_last_marker)
        self.undoMarkerButton.clicked.connect(self.updateMarkerCount)
        self.undoMarkerButton.setFixedSize(400, 40)

        self.clearAllMarkersButton = QPushButton('Delete All Markers')
        self.clearAllMarkersButton.setCursor(Qt.PointingHandCursor)
        self.clearAllMarkersButton.clicked.connect(self.confirmForClearCoordinates)
        self.clearAllMarkersButton.setFixedSize(400, 40)

        # Zoom in/zoom out settings
        self.photo.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.photo.view.setRenderHint(QPainter.Antialiasing)
        self.photo.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.photo.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.photo.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.photo.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.zoomInButton = QPushButton('Zoom In')
        self.zoomInButton.setCursor(Qt.PointingHandCursor)
        self.zoomInButton.setFixedSize(400, 40)

        self.zoomOutButton = QPushButton('Zoom Out')
        self.zoomOutButton.setCursor(Qt.PointingHandCursor)
        self.zoomOutButton.setFixedSize(400, 40)
        self.zoomInButton.clicked.connect(self.photo.zoom_in)
        self.zoomOutButton.clicked.connect(self.photo.zoom_out)

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.countLabel, 0, 0)
        self.smallerGridLayout.addWidget(self.countDisplay, 1, 0)
        self.countDisplay.setFixedSize(400, 40)
        
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
        
        self.smallerGridLayout.addWidget(self.photo.colorChange_Label, 9, 0)
        self.smallerGridLayout.addWidget(self.photo.colorChange, 10, 0)
        self.photo.colorChange.setFixedSize(400, 40)
        
        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        # Keyboard shortcuts
        self.instructions_shortcut = QShortcut(Qt.Key_I, self)
        self.count_shortcut = QShortcut(Qt.Key_C, self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.remove_shortcut = QShortcut(Qt.Key_R, self)
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.zoomin_shortcut = QShortcut(QKeySequence("Ctrl+="), self)
        self.zoomout_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)

        self.instructions_shortcut.activated.connect(self.instruct)
        self.count_shortcut.activated.connect(self.modelStart)
        self.save_shortcut.activated.connect(self.recordInfo)
        self.remove_shortcut.activated.connect(self.photo.remove_marker)
        self.remove_shortcut.activated.connect(self.updateMarkerCount)
        self.undo_shortcut.activated.connect(self.photo.undo_last_marker)
        self.undo_shortcut.activated.connect(self.updateMarkerCount)
        self.zoomin_shortcut.activated.connect(self.photo.zoom_in)
        self.zoomout_shortcut.activated.connect(self.photo.zoom_out)
        
        # Stylesheets
        self.countLabel.setStyleSheet(
            "color: #112d4e;"
        )
        
        self.photo.colorChange_Label.setStyleSheet(
            "color: #112d4e;"
        )

        self.photo.colorChange.setStyleSheet(
            "border: 3px solid;"
            "border-top-color: #00adb5;"
            "border-left-color: #00adb5;"
            "border-right-color: #00adb5;"
            "border-bottom-color: #00adb5;"
            "color: #112d4e;" 
            "padding-right: 8px;"
            "padding-left: 2px;"
            "width: 250px;"
            " font-family: 'Lucida Sans Typewriter';"
            " font-size: 15px;"
            
        )

        self.setStyleSheet(get_basic_styling())


    # Instructions
    def instruct(self):
        self.w = InstructionsWindow()
        self.w.closeButton.clicked.connect(self.instructions_close)
        self.w.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
        self.w.show()

    def instructions_close(self):
        self.w.close()


    # Machine Learning
    def modelStart(self):
        self._modelThread = Thread(target=self.countTentacles)

        if "YOLO Red" not in self.photo.marker_colors:
            if (self.photo.get_filename() == ""):
                msg = QMessageBox(QMessageBox.Warning, "Warning", "Please upload an image.")
                msg.setStyleSheet(get_basic_styling())
                msg.exec_()
            else:
                self.photo.modelDisplay.setText("Running...")
                self._modelThread.start()
        else:
            msg = QMessageBox(QMessageBox.Critical, "Error", "The model has already run.")
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()

        return self
    
    def countTentacles(self):
        self.showLoadingImage.emit()

        # Run the model on the currently displayed photo (in CoralImage)
        resized_img_name = count_tentacles_actual(self.photo.path)
        
        # Add markers based on the labels generated by the model
        # Since you can't call another function within a thread, use signal
        self.placeMarkersCall.emit()

        # Delete the new resized.jpg created in the main folder
        if (os.path.exists(resized_img_name)):
            os.remove(resized_img_name)

        self.hideLoadingImage.emit()
        self.photo.modelDisplay.setText("Finished")
        return None
    
    def placeInitialMarkers(self):
        coordinates = get_coordinates()

        if not coordinates or len(coordinates) <= 5:
            msg = QMessageBox(QMessageBox.Warning, "Warning", 
            """Few to no tentacles were found.\nMake sure you have chosen a clear coral image.""")
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()

            if not coordinates:
                return None

        for pair in coordinates:
            self.photo.add_marker(
                pair[0]*800, pair[1]*500, "YOLO Red"
            )
        
        self.updateMarkerCount()


    # Database
    def recordInfo(self):   
        if self.general_tabs.currentIndex() == 0:
            if not self.photo.get_filename():
                msg = QMessageBox(QMessageBox.Warning, "Warning", "Please upload an image.")
                msg.setStyleSheet(get_basic_styling())
                msg.exec_()
            else:
                self.g = RecordInfoWindow(self.general_username)
                self.g.submitButton.clicked.connect(self.gatheringInfo)
                self.g.submit_shortcut.activated.connect(self.gatheringInfo)

                self.g.setGeometry(int(self.frameGeometry().width()/2) - 150, int(self.frameGeometry().height()/2) - 150, 300, 300)
                self.g.show()

    def gatheringInfo(self):  
        if self.g.notes_Display.text() == "":
            msg = QMessageBox(QMessageBox.Warning, "Warning", "Please enter notes.")
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()

            self.g.close()
            self.recordInfo()
        else:
            try:
                mydb = connectToDatabase()
                
                    
                mycursor = mydb.cursor()
                        
                for i, marker in enumerate(self.photo.markers):
                    self.coordinate_list.append(
                        str(marker.x()) + ', ' + str(marker.y()) 
                        + ' ; ' + str(self.photo.marker_colors[i])
                    )

                coordstring = ' | '.join(self.coordinate_list)

                with open(self.photo.get_path(), "rb") as file:
                    binaryData = file.read()       
                                            
                mycursor.execute(
                    "INSERT INTO image_info VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (
                        self.photo.get_filename(), self.photo.marker_count, 
                        self.general_username, datetime.today(), 
                        coordstring, self.g.get_notes(), binaryData
                    )
                )
                
                self.general_tables.resizeRowsToContents()
            
                mydb.commit()
                
                self.generalDbConnectCalled.emit(self.general_tables)
                self.g.close()
                mydb.close()
                
            except mydb.Error as e:
                print("Failed To Connect to Database")

    def reopenOwnEntry(self, filenameForQuery, coordinatesList):
        self.photo.open_image(filename=filenameForQuery)
        self.clearOldCoordinates()

        placeLoadedCoordinates(coordinatesList.split('|'), self.photo, False)
        self.updateMarkerCount()

        if "YOLO Red" in self.photo.marker_colors:
            self.photo.modelDisplay.setText("Finished")

        self.general_tabs.setCurrentIndex(0)


    # General Updating
    def updateMarkerCount(self):
        self.countDisplay.setText("{0}".format(self.photo.marker_count))
    
    def confirmForClearCoordinates(self):
        if self.photo.marker_count != 0:
            question = QMessageBox()
            response = question.question(
                self,'', "Are you sure you want to delete all the markers?", 
                question.Yes | question.No)
        
            if response == question.Yes:
                while (len(self.photo.markers)) > 0:
                    self.photo.scene.removeItem(self.photo.markers[0])
                    self.photo.markers.pop(0)

                self.clearOldCoordinates()
            else:
                question.close()

    def clearOldCoordinates(self):
        self.photo.marker_count = 0
        self.photo.markers.clear()
        self.photo.marker_colors.clear()
        self.coordinate_list.clear()
        self.photo.modelDisplay.setText("Inactive")
        self.updateMarkerCount()