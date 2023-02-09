import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PhotoLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.photo = QPixmap()
        self.setAcceptDrops(True)
        self.clicked = False

    def setPixmap(self, pixmap):
        self.photo = pixmap
        super().setPixmap(self.photo)
        
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.clicked = True
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        self.clicked = False
        super().mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.clicked:
            self.update()
        super().mouseMoveEvent(event)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.clicked:
            painter = QPainter(self.pix)
            painter.setBrush(Qt.red)
            painter.drawEllipse(event.pos(), 20, 20)

class Image(QWidget):
    
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        
        btn_browse = QPushButton('Browse')
        btn_circle = QPushButton('Add Circle')
        self.pix = QPixmap()
        btn_browse.clicked.connect(self.open_image)
        btn_circle.clicked.connect(self.add_circle)
        
        self.path = ""
        self.file = ""
        
        grid = QGridLayout(self)
        grid.addWidget(btn_browse, 0, 0, Qt.AlignTop)
        grid.addWidget(btn_circle, 0, 1, Qt.AlignTop)
        grid.addWidget(self.photo, 1, 0)
        self.setAcceptDrops(True)
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        grid.addWidget(self.view, 1, 1)
        
    def open_image(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
            self.path = str(filename)
            url = QUrl.fromLocalFile(filename)
            self.file = QFileInfo(filename).fileName()
        
        self.pix = QPixmap(filename)
        self.photo.setPixmap(self.pix.scaledToHeight(400, Qt.SmoothTransformation))
        
    def add_circle(self):
        ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setBrush(QBrush(Qt.red))
        ellipse.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(ellipse)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Image()
    window.show()
    sys.exit(app.exec_())
