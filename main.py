import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import http.server
import json
import asyncio

from botbuilder.schema import (Activity, ActivityTypes)
from botframework.connector import ConnectorClient
from botframework.connector.auth import (MicrosoftAppCredentials,
                                         JwtTokenValidation, SimpleCredentialProvider)
										 
APP_ID = ''
APP_PASSWORD = ''

def hello_admin(msg_body):
    try:
        SUBJECT = 'NOTIFY'
        #msg_body = request.args.get('msg_body')
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
    except:
        return 'ERROR'
    
    print("Email Sent")
    
    #message = 'Subject: {}\n\n{}'.format(SUBJECT, msg_body)

    return 'Email Sent'

class BotRequestHandler(http.server.BaseHTTPRequestHandler):

    @staticmethod
    def __create_reply_activity(request_activity, text):
        return Activity(
            type=ActivityTypes.message,
            channel_id=request_activity.channel_id,
            conversation=request_activity.conversation,
            recipient=request_activity.from_property,
            from_property=request_activity.recipient,
            text=text,
            service_url=request_activity.service_url)

    def __handle_conversation_update_activity(self, activity):
        self.send_response(202)
        self.end_headers()
        if activity.members_added[0].id != activity.recipient.id:
            credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
            reply = BotRequestHandler.__create_reply_activity(activity, 'Hello and welcome to the echo bot!')
            connector = ConnectorClient(credentials, base_url=reply.service_url)
            connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_message_activity(self, activity):
        self.send_response(200)
        self.end_headers()
        credentials = MicrosoftAppCredentials(APP_ID, APP_PASSWORD)
        connector = ConnectorClient(credentials, base_url=activity.service_url)
        print ("INPUT : ",activity.text)

        status_email = hello_admin(activity.text)

        if status_email =="ERROR":
            reply = BotRequestHandler.__create_reply_activity(activity, 'EMAIL NOT SENT FOR THIS : %s' % activity.text)
            connector.conversations.send_to_conversation(reply.conversation.id, reply)
        else:
            reply = BotRequestHandler.__create_reply_activity(activity, 'EMAIL SENT WITH TEXT: %s' % activity.text)
            connector.conversations.send_to_conversation(reply.conversation.id, reply)

    def __handle_authentication(self, activity):
        credential_provider = SimpleCredentialProvider(APP_ID, APP_PASSWORD)
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(JwtTokenValidation.authenticate_request(
                activity, self.headers.get("Authorization"), credential_provider))
            return True
        except Exception as ex:
            self.send_response(401, ex)
            self.end_headers()
            return False
        finally:
            loop.close()

    def __unhandled_activity(self):
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(str(body, 'utf-8'))
        activity = Activity.deserialize(data)

        if not self.__handle_authentication(activity):
            return

        if activity.type == ActivityTypes.conversation_update.value:
            self.__handle_conversation_update_activity(activity)
        elif activity.type == ActivityTypes.message.value:
            self.__handle_message_activity(activity)
        else:
            self.__unhandled_activity()


try:
    SERVER = http.server.HTTPServer(('localhost', 9000), BotRequestHandler)
    print('Started http server on localhost:9000')
    SERVER.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    SERVER.socket.close()
