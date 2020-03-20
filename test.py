import serial
import mysql.connector
import time
import re
import datetime

dbConn = mysql.connector.connect(host="localhost", user="root", passwd="")
cursor = dbConn.cursor()
date = datetime.datetime.now().strftime("%b") + "_" + datetime.datetime.now().strftime(
    "%d") + "_" + datetime.datetime.now().strftime("%Y")
cursor.execute("Use attendance")
cursor.execute("Alter table attend add " + date + " VARCHAR(20)")
device = 'COM8 (Arduino Uno)'  # this will have to be changed to the serial port you are using
try:
    print("Trying...", device)
    arduino = serial.Serial("COM8", 9600)
except:
    print("Failed to connect on", device)
while True:
    time.sleep(1)
    try:
        data = arduino.read(30)
        print("Marked Present..!!")
        pieces = data.decode('utf8')
        k = re.split(r'[:,\s]\s*', pieces)
        try:
            cursor = dbConn.cursor()
            cursor.execute("SELECT Name FROM attend where UID = '" + k[2] + "'")
            check = cursor.fetchall()
            dataa = ''.join(check[0])
            if (dataa != None):
                cursor.execute("Update attend set " + date + " = 'Present' where Name = '"+dataa+"' ")
                dbConn.commit()
            stop = input("Enter Q/q to stop else press any key :")
            if(stop.lower() == "q"):
                break
            else :
                continue
        except mysql.connector.IntegrityError:
            print("failed to insert data")

    except:
        print("Error")
    finally:
        cursor.execute("SELECT Name FROM attend WHERE "+date+" is NULL ")
        x = cursor.fetchall()
        print(x)
        print("Students Absent : ")
        for a in range(len(x)):
            print(x[a])
