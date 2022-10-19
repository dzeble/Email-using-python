from email.message import EmailMessage
import email
import ssl 
import smtplib
import mysql.connector
import pandas as pd
import schedule
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def job():    #put the code in a function called 'job' to make the scheduling easier
    email_sender = 'sender@gmail.com'  #email of sender
    email_password = '' #16 digit password for third party apps 
    email_receiver = 'receiver@outlook.com'  #email of receiver
    subject = 'This is not a spam message'
    body = """
War it is'nt good for absolutely nothing
"""

    mail = EmailMessage()
    mail['From'] = email_sender
    mail['To'] = email_receiver
    mail['Subject'] = subject
    mail.set_content(body)
    mail["Bcc"] = email_receiver  


    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",  #mysql password goes here
        database = 'svenschema'#your selected database)

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM people") #your selected table

    myresult = mycursor.fetchall()

    XL_file = [] #empty array to get the rows of the table

    for row in myresult:
        XL_file.append(row)
        print(row)

    df = pd.DataFrame(XL_file)
    df_csv = df.to_csv('C:/Users/Sven/Desktop/Mail/NewExcelFile.csv')  #convert to a csv file

    with open("NewExcelFile.csv", "rb") as fp:
        filedata = fp.read()
        file_name = fp.name
        mail.add_attachment(
            filedata, maintype = 'application', subtype = 'csv', filename =file_name)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,mail.as_string())


schedule.every(10).seconds.do(job)  #schedule for the email to be sent every 10 seconds


while True:
    schedule.run_pending()
    time.sleep(1)