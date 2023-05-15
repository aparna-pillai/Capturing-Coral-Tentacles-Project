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

        self.error_messages = ["No associated user found. Try a different name.",
                              "Incorrect code. Try again."]

    def check_code_on_initial_login(self):
        # try:
            #self.lineEdit = self.userTextBox.text()
            #self.lineEdit_2 = self.codeTextBox.text()
            
            mydb = connectToDatabase()
            
            mycursor = mydb.cursor()

            sql =  "SELECT users_name, users_code FROM users WHERE users_name = '%s'" % self.lineEdit.text()
            mycursor.execute(sql)
            myresult1 = mycursor.fetchall()
            
            if len(myresult1) == 0:
                QMessageBox.about(self, "Error", self.error_messages[0])

            else:
                code = ''.join(myresult1[0])
               
                mydb.close()

                if self.lineEdit_2.text() == code[-10:]:
                    return code[:-10]
                else:
                    QMessageBox.about(self, "Error", self.error_messages[1])
                    return None


        # except mydb.Error as e:
        #    print("Failed To Connect to Database")

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("You entered the wrong username or code.")
        msg.setIcon(QMessageBox.critical)
        msg.setStandardButtons(QMessageBox.Retry)
        msg.setInformativeText("If you are having trouble logging in, contact Ms. Kennedy for a new username or code.")
        msg = QMessageBox(Login_Window)
