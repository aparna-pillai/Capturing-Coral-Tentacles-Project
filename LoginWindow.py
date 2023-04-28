import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mysql.connector as mc
import os

class Login_Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.generalLayout = QGridLayout()

        self.user_label = QLabel("Username:")
        self.userTextBox = QLineEdit()
        self.code_label = QLabel("Code:")
        self.codeTextBox = QLineEdit()

        self.deniedLabel = QLabel("Access Denied.")
        self.deniedLabel.hide() # Only show if the code is incorrect

        self.enteredUsername = ""
        self.enteredCode = ""

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.user_label, 0, 0)
        self.smallerGridLayout.addWidget(self.userTextBox, 0, 1)
        self.smallerGridLayout.addWidget(self.code_label, 1, 0)
        self.smallerGridLayout.addWidget(self.codeTextBox, 1, 1)
        self.generalLayout.addLayout(self.smallerGridLayout, 0, 0)

        self.generalLayout.addWidget(self.deniedLabel)

        self.submitButtonLogin = QPushButton("Submit")
        self.generalLayout.addWidget(self.submitButtonLogin, 2, 0)

        self.setLayout(self.generalLayout)


        # Stylesheets
        self.deniedLabel.setStyleSheet(
            "color: red;"
        )

    def check_code_on_initial_login(self):
        try:
            self.enteredUsername = self.userTextBox.text()
            self.enteredCode = self.codeTextBox.text()
            # print(self.enteredUsername, self.enteredCode)
            
            mydb = mc.connect(
                host = os.environ.get('HOST'),
                user = os.getenv('NAME'),
                password = os.getenv('PASSWORD'),
                database = os.getenv('DATABASE')
            )
            mycursor = mydb.cursor()

            mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % self.enteredUsername)
            myresult = mycursor.fetchall()

            if len(myresult) == 0:
                self.deniedLabel.setText("Invalid username. Try again.")
                self.deniedLabel.show()
                mydb.close()
            else:
                # print(myresult)
                # print(myresult[0])
                str = ''.join(myresult[0])
                # print(str)

                mydb.close()

                if self.enteredCode == str:
                    return True
                else:
                    self.deniedLabel.setText("Incorrect code. Try again.")
                    self.deniedLabel.show()
                    return False

        except mydb.Error as e:
           print("Failed To Connect to Database")            
        
# Only for testing
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LoginWindow()
#     window.show()

#     sys.exit(app.exec_())