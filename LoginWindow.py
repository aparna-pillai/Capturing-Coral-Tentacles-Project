from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from loginUI import Ui_Form
import sys

from connectToDatabase import *

class Login_Window(QWidget, Ui_Form):
    
    def __init__(self):

        super(Login_Window, self).__init__()
        self.setupUi(self)

        # super().__init__()

        # self.setWindowTitle("Log In")
        # self.generalLayout = QGridLayout()

        # self.title_label = QLabel("Login")
        # self.title_label.setStyleSheet(
        #     "font-size: 20px;"
        #     "font-weight: bold;"
        # )

        # self.user_label = QLabel("Username:")
        # self.userTextBox = QLineEdit()

        # self.code_label = QLabel("Code:")
        # self.codeTextBox = QLineEdit()
        # self.codeTextBox.setEchoMode(QLineEdit.Password)

        # self.deniedLabel = QLabel("")
        # self.deniedLabel.hide() # Only show if the code is incorrect

        # self.enteredUsername = ""
        # self.enteredCode = ""

        # self.error_messages = ["No associated user found. Try a different name.",
        #                       "Incorrect code. Try again."]

        # self.smallerGridLayout = QGridLayout()

        # self.smallerGridLayout.addWidget(self.title_label, 1, 0)
        # self.smallerGridLayout.addWidget(self.user_label, 1, 1)
        # self.smallerGridLayout.addWidget(self.userTextBox, 1, 2)
        # self.smallerGridLayout.addWidget(self.code_label, 2, 1)
        # self.smallerGridLayout.addWidget(self.codeTextBox, 2, 2)
        # self.generalLayout.addLayout(self.smallerGridLayout, 0, 0)
        

        #self.generalLayout.addWidget(self.deniedLabel)

        # self.submitButtonLogin = QPushButton("Submit")
        # self.generalLayout.addWidget(self.submitButtonLogin, 2, 0)

        # self.setLayout(self.generalLayout)

        # # Stylesheets
        # self.deniedLabel.setStyleSheet(
        #     "color: red;"
        # )

        # self.userTextBox.setStyleSheet(
        #     "color: blue;"
        # )

        # self.codeTextBox.setStyleSheet(
        #     "color: blue;"
        # )

    def check_code_on_initial_login(self):
        try:
            #self.lineEdit = self.userTextBox.text()
            #self.lineEdit_2 = self.codeTextBox.text()
            
            mydb = connectToDatabase()
            
            mycursor = mydb.cursor()

            sql =  "SELECT users_name, users_code FROM users WHERE users_name = '%s'" % self.lineEdit.text()
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            
            if len(myresult1) == 0:
                self.deniedLabel.setText(self.error_messages[0])
                self.deniedLabel.show()
                
            else:
                code = ''.join(myresult1[0])
               
                mydb.close()

                if self.lineEdit_2.text() == code[-10:]:
                    print(code[:-10])
                    return code[:-10]
                else:
                    self.deniedLabel.setText(self.error_messages[1])
                    self.deniedLabel.show()
                    return None

        except mydb.Error as e:
           print("Failed To Connect to Database")