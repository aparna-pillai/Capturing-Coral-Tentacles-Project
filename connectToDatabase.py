import os
import mysql.connector as mc

# function
def connectToDatabase():
    mydb = mc.connect(
        host=os.environ.get('HOST'),
        user=os.getenv('NAME'),
        password=os.getenv('PASSWORD'), 
        database=os.getenv('DATABASE')             
    )
    return mydb