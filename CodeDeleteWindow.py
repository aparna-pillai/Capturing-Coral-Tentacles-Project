import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from basic_styling import *

class CodeDeleteWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete")
        icon_pixmap = QPixmap("style_images/Actual Final Logo.png")
        self.setWindowIcon(QIcon(icon_pixmap))
        self.generalLayout = QGridLayout()

        self.label = QLabel("Enter your code")
        self.codeTextBox = QLineEdit()
        self.codeTextBox.setEchoMode(QLineEdit.Password)

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.label, 0, 0)
        self.smallerGridLayout.addWidget(self.codeTextBox, 0, 1)
        self.generalLayout.addLayout(self.smallerGridLayout, 0, 0)

        self.submitButtonLogin = QPushButton("Submit")
        self.submitButtonLogin.setCursor(Qt.PointingHandCursor)
        self.generalLayout.addWidget(self.submitButtonLogin, 1, 0)
        self.submit_shortcut = QShortcut(Qt.Key_Return, self)

        self.setLayout(self.generalLayout)

        self.setStyleSheet(get_basic_styling())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeDeleteWindow()
    window.show()

    sys.exit(app.exec_())