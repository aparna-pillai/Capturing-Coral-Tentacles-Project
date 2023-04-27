import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Login_Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.generalLayout = QGridLayout()

        self.label = QLabel("Enter your code")
        self.codeTextBox = QLineEdit()

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.label, 0, 0)
        self.smallerGridLayout.addWidget(self.codeTextBox, 0, 1)
        self.generalLayout.addLayout(self.smallerGridLayout, 0, 0)

        self.submitButtonLogin = QPushButton("Submit")
        self.generalLayout.addWidget(self.submitButtonLogin, 1, 0)

        self.setLayout(self.generalLayout)

    def checkCode(self):
        """
        For the real function:
        1. Check if the code is in the database.
        2. If it is, get the name associated with that code.
        3. Close this login window and open main window with coral counting function.
            a. The person's name should be displayed at the top right.
        """

        enteredCode = self.codeTextBox.text()
        print(enteredCode)
        msg = QMessageBox()

        if enteredCode == "abc":
            msg.setWindowTitle("Access Granted :)")
            msg.setText("Yes, the correct code is abc! Only for testing, though.")
        else:
            msg.setWindowTitle("Access Denied :(")
            msg.setText("Sorry, that is not the correct code.")

        msg.exec_()
        

# Only for testing
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LoginWindow()
#     window.show()

#     sys.exit(app.exec_())