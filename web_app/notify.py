import smtplib, email

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'rohan.raut@mmit.edu.in'
sender_name = 'Rohan Raut'
password = 'chzhpfltnmgwnfnv'


def send_notification(sender_name, receiver_email, subject, body):
    try:
        smtpObj = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtpObj.starttls()
        smtpObj.login(sender_email, password)

        message = MIMEMultipart()
        message["From"] = sender_name
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        smtpObj.sendmail(sender_email, receiver_email, text)

        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
