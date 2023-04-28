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

        #self.deniedLabel = QLabel("Access Denied.")
        #self.deniedLabel.hide() # Only show if the code is incorrect

        self.enteredUsername = ""
        self.enteredCode = ""

        self.smallerGridLayout = QGridLayout()
        self.smallerGridLayout.addWidget(self.user_label, 0, 0)
        self.smallerGridLayout.addWidget(self.userTextBox, 0, 1)
        self.smallerGridLayout.addWidget(self.code_label, 1, 0)
        self.smallerGridLayout.addWidget(self.codeTextBox, 1, 1)
        self.generalLayout.addLayout(self.smallerGridLayout, 0, 0)

        #self.generalLayout.addWidget(self.deniedLabel)

        self.submitButtonLogin = QPushButton("Submit")
        self.generalLayout.addWidget(self.submitButtonLogin, 2, 0)

        self.setLayout(self.generalLayout)


        # # Stylesheets
        # self.deniedLabel.setStyleSheet(
        #     "color: red;"
        # )

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
                QMessageBox.about(self, "Warning", "Incorrect username or code. Try Again")
                mydb.close()
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
                    print(code)
                    # mycursor.execute("SELECT users_name FROM users WHERE users_code = '%s'" % code)
                    # myresult1 = mycursor.fetchall()
                    # name = ''.join(myresult1[0])
                    print(code[:-10])
                    return code[:-10]
                else:
                    QMessageBox.about(self, "Warning", "Incorrect username or code. Try Again")
                    return None

        except mydb.Error as e:
           print("Failed To Connect to Database")            
        
# Only for testing
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = LoginWindow()
#     window.show()

#     sys.exit(app.exec_())