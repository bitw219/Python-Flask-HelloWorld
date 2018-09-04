from flask import Flask
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'SHUBHAM IS HERE'

if __name__ == '__main__':
  app.run()
