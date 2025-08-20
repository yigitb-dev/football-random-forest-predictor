import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP('smtp.gmail.com',587)


server.ehlo()
server.starttls()



with open('password.txt','r') as f:
    password = f.read()

with open('message.txt','r') as f:
    message = f.read()

server.login('yigitbicakci08@gmail.com',password)

msg = MIMEMultipart()
msg['from'] = 'YigitBicakci'
msg['to'] = 'yigitbicakci3@gmail.com'
msg['Subject'] = input("Subject: ")

msg.attach(MIMEText(message,'plain'))

text = msg.as_string()
server.sendmail('yigitbicakci08@gmail.com','yigitbicakci3@gmail.com',text)