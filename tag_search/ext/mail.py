import os
from flask import current_app as app
from flask_mail import Mail, Message
#TODO write a recover email function
def send_email (title, body, recipient):
    mail = Mail(app)
    msg = Message(
            subject = title,
            sender =("Me", os.getenv('MAIL_USERNAME')),
            recipients = [recipient],
            html = body
            )
    mail.send(msg)