import re
import smtplib
import csv
from email.mime.text import MIMEText

# Email regex validation
EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")
# smtp settings
SERVER = 'smtp.gmail.com'
PORT = 587
""" Dont forget to turn on 
    https://www.google.com/settings/security/lesssecureapps for your gmail
"""


class Greeting(object):

    def __init__(self):
        with open('settings.txt') as f:
            self.settings = dict(line.rstrip().split(None, 1) for line in f)

    def compose_message(self, person_details):
        greeting_template = open('templates/new_year.txt', 'rb')
        first_name = person_details['first_name']
        last_name = person_details['last_name']
        message = greeting_template.read().format(first_name, last_name)
        msg = MIMEText(message)
        greeting_template.close()
        msg['Subject'] = self.settings['subject']
        msg['From'] = self.settings['from_email']
        msg['To'] = person_details['email']
        return msg

    def setup_smtp_server(self):
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.ehlo()
        from_email = self.settings['from_email']
        password = self.settings['password']
        server.login(from_email, password)
        return server

    def send_email(self):
        server = self.setup_smtp_server()
        contacts = open('contacts.csv', 'rb')
        reader = csv.DictReader(contacts)
        for person_details in reader:
            to_email = person_details['email']
            message = self.compose_message(person_details).as_string()
            server.sendmail(self.settings['from_email'], [to_email], message)
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
    print "Sending greetings .. . . ."
    greeting = Greeting()
    greeting.send_email()


if __name__ == '__main__':
    main()
