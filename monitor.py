import time
import smtplib
import yaml

from keras.callbacks import Callback
from email.mime.text import MIMEText
from pprint import pformat

class EmailMonitor(Callback):
    def __init__(self, recipient_email):
        super(EmailMonitor, self).__init__()

        self.recipient_email = recipient_email
        sender_info = yaml.load(open('secrets.yaml'))
        self.sender_email = sender_info['sender']['email_address']
        self.sender_pwd = sender_info['sender']['password']

        self.previous_stats_email = None
        self.current_epoch = 0

    def _send_email(self, body):
        msg = MIMEText(body)

        msg['Subject'] = self.email_header
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.sender_email, self.sender_pwd)

        server.sendmail(self.sender_email, self.recipient_email, msg.as_string())
        server.quit()


    def on_train_begin(self, logs=None):
        self.train_start_time = time.strftime("%Y-%m-%d %H:%M")
        self.email_header = "Monitoring for model that started training at {0}\n".format(self.train_start_time)


    def on_epoch_end(self, epoch, logs=None):
        self.current_epoch += 1

        if logs is not None:
            current_stats_email = pformat(logs)
            email_body = "Current stats (epoch {0}):\n".format(self.current_epoch) + current_stats_email
            if self.previous_stats_email:
                email_body += "\n\nPrevious stats (epoch {0}):\n".format(self.current_epoch-1) + self.previous_stats_email

            self._send_email(email_body)
            self.previous_stats_email = current_stats_email


    def on_train_end(self, logs=None):
        email_body = "Model finished training at {0}".format(time.strftime("%Y-%m-%d %H:%M"))
        self._send_email(email_body)
