from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PIL import Image as ImagePIL
import os

from Image2 import *
from recordTab import RecordTab
from coral_count import count_tentacles_actual, get_count, get_coordinates

class GeneralTab(QWidget):

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

        # Initial layout creation and button connection
        self.generalLayout = QGridLayout()
        
        self.photo = Image2()
        self.generalLayout.addWidget(self.photo, 0, 0)

        self.g = None

        self.instructionsButton = QPushButton("Instructions")
        self.instructionsButton.clicked.connect(self.instruct)

        self.savePicButton = QPushButton("Save Picture to Record")
        self.savePicButton.clicked.connect(RecordTab.recordInfo)

        self.countButton = QPushButton("Count")
        self.countButton.clicked.connect(self.countTentacles)

        self.countLabel = QLabel("Tentacle Count:")
        self.countDisplay = QLineEdit("{0}".format(int(self.photo.get_marker_count)))

        self.removeMarkerButton = QPushButton("Remove Marker")
        self.removeMarkerButton.clicked.connect(self.photo.remove_marker)
        self.removeMarkerButton.clicked.connect(self.updateMarkerCount)

        self.undoMarkerButton = QPushButton('Undo Last Marker')
        self.undoMarkerButton.clicked.connect(self.photo.undo_last_marker)
        self.undoMarkerButton.clicked.connect(self.updateMarkerCount)

        # Adding buttons to layout
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

        self.generalLayout.addLayout(self.smallGridLayout, 0, 1)

        # Stylesheets
        self.countLabel.setStyleSheet(
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

        self.setStyleSheet(
            "QLabel {color: blue;}"
        )

        self.setLayout(self.generalLayout)


    def get_photo_object(self):
        return self.photo
    
    def get_g(self):
        return self.g

    def instruct(self):
        msg = QMessageBox.about(
            self, "Instructions", 
            '''
            Instructions :
            1. Click on Browse to select your image for coral counting.
            2. Click Count for the program to generate the markers
                and count.
            3. To edit the markers, click on any of the markers and click
                Remove or Add Marker. The numerical Count will update 
                automatically.
            4. To save your count, click Save Count. Your Count will now 
                be saved in the Record/Log.
            5. You can delete the saved count from the Record by 
                clicking Delete Count.
            6. Here are some useful keyboard shortcuts:

            On Main tab:
                B - Browse photos
                C - Count
                Click - Add marker
                R - Remove selected marker
                Ctrl+Z (Windows), Command+Z (Mac) - Undo most 
                    recent marker
                Ctrl+S (Windows), Command+S (Mac) - Save photo 
                    to record
                I - Instructions

            On Record tab:
                Enter (Windows), return (Mac) - Load from database
                Delete (Windows), fn delete (Mac) - Delete selected 
                    database entry

            Tab - Switch between tabs
            Ctrl+W (Windows), Command+W (Mac) - Close application
            ''' 
        )
        
        return msg
    
    def countTentacles(self):
        if (self.photo.get_filename() == ""):
            QMessageBox.about(self, "Warning", "Please upload an image.")
        else:
            # Run the model on the currently displayed photo (in Image2)
            count_tentacles_actual(self.photo.path)
            img = ImagePIL.open(self.photo.path)
            
            # Add markers based on the labels generated by the model
            self.placeInitialMarkers(img.width, img.height)

            # Get tentacle count
            self.count = get_count()
            self.countDisplay.setText(str(get_count()))

            # Delete the new resized.jpg created in the main folder
            if (os.path.exists('resized.jpg')):
                os.remove('resized.jpg')

    def placeInitialMarkers(self, photo_width, photo_height):
        coordinates = get_coordinates()

        # Clear out all old results
        self.photo.marker_count = 0
        self.photo.markers.clear()
        self.list.clear()

        for pair in coordinates:
            self.photo.add_marker(
                pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5), 
                QColor(245, 96, 42)
            )
            self.list.append(
                "({}, {})".format(pair[0]*(photo_width/1.6), pair[1]*(photo_height/1.5))
            )

    def updateMarkerCount(self):
        self.countDisplay.setText("{0}".format(self.photo.marker_count))