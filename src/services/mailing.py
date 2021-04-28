import smtplib
import ssl
from email.message import EmailMessage

from flask import current_app


class Email:
    """Send E-Mail from Uberspace.
    More details at https://manual.uberspace.de/mail-access.html
    https://docs.python.org/3/library/email.examples.html
    """
    def __init__(self, subject, text):
        self.sender = current_app.config['MAIL_SENDER']
        self.recipient = current_app.config['MAIL_RECIPIENT']
        self.subject = subject
        self.text = text
        self.server = current_app.config['MAIL_SERVER']
        self.port = current_app.config['MAIL_PORT']
        self.login = current_app.config['MAIL_LOGIN']
        self.password = current_app.config['MAIL_PASSWORD']

    def send(self):
        msg = EmailMessage()
        msg.set_content(self.text)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient

        server = smtplib.SMTP(self.server, self.port)
        context = ssl.create_default_context()

        try:
            server.starttls(context=context)  # Secure the connection
            server.login(self.login, self.password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False
