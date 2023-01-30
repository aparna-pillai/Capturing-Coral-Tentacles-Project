import sys

from PhotoLabel import PhotoLabel

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

from PIL import Image, ImageTk

import cv2 as cv
import numpy as np

COUNT = 0
PATH = ""

class GalleryInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gathering Gallery Info")
        # Create a top-level layout
        layout = QVBoxLayout()
        self.label = QLabel("New Window")
        self.setLayout(layout)
    
    
