import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import mysql.connector as mc
import os
import time

class Login_Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.generalLayout = QGridLayout()

        self.title_label = QLabel("Login")
        self.title_label.setStyleSheet(
            "font-size: 20px;"
            "font-weight: bold;"
        )

        self.user_label = QLabel("Username:")
        self.userTextBox = QLineEdit()
        self.code_label = QLabel("Code:")
        self.codeTextBox = QLineEdit()
        self.codeTextBox.setEchoMode(QLineEdit.Password)

        self.deniedLabel = QLabel("")
        print(self.deniedLabel.text())
        self.deniedLabel.hide() # Only show if the code is incorrect

        self.enteredUsername = ""
        self.enteredCode = ""

        self.error_messages = ["No associated user found. Try a different name.",
                              "Incorrect code. Try again."]

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.title_label, 0, 0)
        self.smallerGridLayout.addWidget(self.user_label, 1, 0)
        self.smallerGridLayout.addWidget(self.userTextBox, 1, 1)
        self.smallerGridLayout.addWidget(self.code_label, 2, 0)
        self.smallerGridLayout.addWidget(self.codeTextBox, 2, 1)
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

            # mycursor.execute("SELECT users_code FROM users WHERE users_name = '%s'" % self.enteredUsername)
            # myresult = mycursor.fetchall()
            
            # mycursor = mydb.cursor()
            sql =  "SELECT users_name, users_code FROM users WHERE users_name = '%s'" % self.enteredUsername
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            
            if len(myresult1) == 0:
                self.deniedLabel.setText(self.error_messages[0])
                self.deniedLabel.show()
                
                # QMessageBox.about(self, "Warning", "Incorrect username or code. Try Again")
                # mydb.close()
            else:
                print(myresult1)
                print(myresult1[0])
                #print(myresult1[1])
                code = ''.join(myresult1[0])
               
                mydb.close()

                print(code)
                print(code[-10:])
                #print(self.g.get_code())
                if self.enteredCode == code[-10:]:
                    # print(code)
                    # mycursor.execute("SELECT users_name FROM users WHERE users_code = '%s'" % code)
                    # myresult1 = mycursor.fetchall()
                    # name = ''.join(myresult1[0])
                    # print(code[:-10])
                    return code[:-10]
                else:
                    # QMessageBox.about(self, "Warning", "Incorrect username or code. Try Again")
                    self.deniedLabel.setText(self.error_messages[1])
                    self.deniedLabel.show()

                    return None

        except mydb.Error as e:
           print("Failed To Connect to Database")