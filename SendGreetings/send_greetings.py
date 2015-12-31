import re
import smtplib
from email.mime.text import MIMEText

EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")
SERVER = 'smtp.gmail.com'
PORT = 587
# Dont forget to turn on https://www.google.com/settings/security/lesssecureapps for your gmail


class Greeting(object):

    def __init__(self):
        self.message = self.get_message()
        with open('settings.txt') as f:
            self.settings = dict(line.rstrip().split(None, 1) for line in f)
        self.message['subject'] = self.settings['subject']
        # validate_settings(self.settings)

    def get_message(self):
        greeting_template = open('templates/new_year.txt', 'rb')
        msg = MIMEText(greeting_template.read())
        greeting_template.close()
        return msg

    def setup_smtp_server(self):
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        from_email = self.settings['from_email']
        password = self.settings['password']
        server.login(from_email, password)
        return server

    def send_email(self):
        server = self.setup_smtp_server()
        server.sendmail(self.settings['from_email'], ['omkarvijay5@gmail.com'], self.message.as_string())
        server.quit()


def get_email():
    while 1:
        email = raw_input("Please Enter your email:")
        if not EMAIL_REGEX.match(email):
            print "Please enter proper email"
        else:
            break
    return email


def main():
    print "Welcome to send_greetings........!!!!"
    # email = get_email()
    # message = get_message()
    greeting = Greeting()
    greeting.send_email()


if __name__ == '__main__':
    main()
