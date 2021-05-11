#!/usr/bin/python
#-*- encoding:utf-8 -*-

import os
import sys
import json
import time
import email
import imaplib
import smtplib
import ssl
from datetime import datetime
from email.header import Header, decode_header, make_header
from smtplib import SMTPAuthenticationError
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate

arg = sys.argv[1:]

class Watchdog:
    def __init__(self):
        self.refresh_data()

    def refresh_data(self):
        with open('config.json',) as self.f:
            self.data = json.load(self.f)
        self.username = self.data["USERNAME"]
        self.password = self.data["PASSWORD"]
        self.emails = self.data['EMAILS']
        self.file  = self.data['FILE']
        self.last_check = self.data['LAST_CHECK']
        self.deadline = self.data['DEADLINE']
        self.token = self.data['TOKEN']

    def update_conf(self):
        with open('config.json', 'w') as conf:
            json.dump(self.data, conf, indent=4)

    def get_mail(self):
        self.refresh_data()
        self.emails = []
        ids=[]

        self.mail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.mail.login(self.username, self.password)
        self.mail.select('inbox')
        status, data = self.mail.search(
            None, 'UNSEEN', 'FROM', 'email_address')
        for block in data:
            ids += block.split()
        ids.reverse()
        if len(ids) > 0:
            for item in ids:
                status, data = self.mail.fetch(item, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        message = email.message_from_bytes(response_part[1])
                        try:
                            mail_subject = str(make_header(decode_header(message['subject'])))
                            print(mail_subject)
                        except TypeError:
                            continue
                        if mail_subject == self.token:
                            self.reset()
                            return True
        return False

    def send_response(self, content):
        self.refresh_data()
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context)
        server.login(self.username, self.password)
        msg = MIMEText(content)
        msg['Subject'] = "From Your Dead Man's Switch"
        msg['To'] = "email_address"
        msg['From'] = self.username

        server.sendmail(
            self.username, "email_address", msg.as_string())

    def check(self):
        if self.get_mail():
            print(True)
            self.refresh_data()
            text = """
Congratulations, you've survived another week!
Your next deadline is: %s""" %(datetime.fromtimestamp(self.deadline))
            self.send_response(text)
        else:
            print(False)
            now = time.time()
            self.data['LAST_CHECK'] = time.time()
            self.update_conf()
            if (self.deadline - now) < 0:
                self.emergency()
                time.sleep(10)
                os.system("sudo poweroff")
            elif (self.deadline - now) <= 172800:
                text = """
Hi,
This is a reminder for you to send your token.
Here's your token in case you forgot it: %s
Your current deadline is: %s
I hope you're still alive.
Have a nice day.""" %(self.token, datetime.fromtimestamp(self.deadline))
                self.send_response(text)

    def reset(self):
        self.refresh_data()
        now = time.time()
        self.data['LAST_CHECK'] = now
        self.data['DEADLINE'] = now + 604800
        self.update_conf()

    def emergency(self):
        self.refresh_data()
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context)
        server.login(self.username, self.password)
        for addr in self.emails:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = addr
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = "subject"
            text = """Emergency message"""
            msg.attach(MIMEText(text))
            with open(self.file, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=os.path.basename(self.file))

            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(self.file)
            msg.attach(part)
            server.sendmail(
                self.username, addr, msg.as_string())

if __name__ == "__main__":
    if os.path.dirname(__file__):
        os.chdir(os.path.dirname(__file__))
    w = Watchdog()
    if "--reset" in arg:
        w.reset()
        exit()
    w.check()
## Implement reset function
