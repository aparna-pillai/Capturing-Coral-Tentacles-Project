from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from loginUI import Ui_Form

from connectToDatabase import *
from basic_styling import *

class Login_Window(QWidget, Ui_Form):
    
    def __init__(self):

        super(Login_Window, self).__init__()
        
        self.setupUi(self)

        self.error_messages = ["No associated user found. Try a different name.",
                              "Incorrect code. Try again."]

    def check_code_on_initial_login(self):
        mydb = connectToDatabase()
        
        mycursor = mydb.cursor()

        sql =  "SELECT users_name, users_code FROM users WHERE users_name = '%s'" % self.lineEdit.text()
        mycursor.execute(sql)
        myresult1 = mycursor.fetchall()
        
        if len(myresult1) == 0:
            msg = QMessageBox(QMessageBox.Critical, "Error", self.error_messages[0])
            msg.setStyleSheet(get_basic_styling())
            msg.exec_()
        else:
            code = ''.join(myresult1[0])
            
            mydb.close()

            if self.lineEdit_2.text() == code[-10:]:
                return code[:-10]
            else:
                msg = QMessageBox(QMessageBox.Critical, "Error", self.error_messages[1])
                msg.setStyleSheet(get_basic_styling())
                msg.exec_()

                return None

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("You entered the wrong username or code.")
        msg.setIcon(QMessageBox.critical)
        msg.setStandardButtons(QMessageBox.Retry)
        msg.setInformativeText("If you are having trouble logging in, contact Ms. Kennedy for a new username or code.")
        msg = QMessageBox(Login_Window)
