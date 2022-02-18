import mysql.connector
from dotenv import load_dotenv
import os

def connection_establish(db_pass):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE HeartBeat")
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        if x[0] == 'HeartBeat':
            return True
    return False

def main():
    load_dotenv()
    db_pass = os.environ.get('DB_PASS')
    if connection_establish(db_pass):
        print("Successfully Established Connection")
    else:
        print("Something went wrong")


if __name__ == "__main__":
    main()
