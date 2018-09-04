from flask import Flask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def hello_world():
  msg_body = 'Farhan IS HERE'
  SUBJECT = 'NOTIFY'
  msg = MIMEMultipart()
  msg.attach(MIMEText(msg_body,'plain'))
  message = 'Subject: {}\n\n{}'.format(SUBJECT, msg_body)
  server = smtplib.SMTP('smtp.gmail.com',25)
  server.ehlo()
  server.starttls()
  server.ehlo()
  server.login("aatish.jain@ellicium.com","9921610239")
  server.sendmail("aatish.jain@ellicium.com",['aatish.jain@ellicium.com','shubham.shirude@ellicium.com'],message)
  server.quit()
  return msg_body

if __name__ == '__main__':
  app.run()
