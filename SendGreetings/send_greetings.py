# !/usr/bin/python
import re
import smtplib
import csv
from email.mime.text import MIMEText

"""
send_greetings is a small python app which was developed to make ease in sending
greetings for each and every occassion to a bunch of emails.

The app expects few things to be in right place before executing.
Only thing you need to configure is the settings.txt file which has from_email
and password which should be given properly
Dont forget to turn on 
    https://www.google.com/settings/security/lesssecureapps 
for your gmail account Thats it ..!!!
"""
# Email regex validation
EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")
# smtp settings
SERVER = 'smtp.gmail.com'
PORT = 587


class Greeting(object):

    def __init__(self):
        with open('settings.txt') as f:
            self.settings = dict(line.rstrip().split(None, 1) for line in f)
        self.validate_email()

    def compose_message(self, person_details):
        """
        Composes unique message for individual user from csv
        """
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

    def config_smtp_server(self):
        """
        SMTP configuration for sending email. Authentication Check for the specified email
        """
        server = smtplib.SMTP(SERVER, PORT)
        server.starttls()
        server.ehlo()
        from_email = self.settings['from_email']
        password = self.settings['password']
        server.login(from_email, password)
        return server

    def send_email(self):
        """
        Reads email ids from contacts.csv and users from csv file. Composes individual message
        and sends greetings to individual
        """
        server = self.config_smtp_server()
        contacts = open('contacts.csv', 'rb')
        reader = csv.DictReader(contacts)
        for person_details in reader:
            to_email = person_details['email']
            message = self.compose_message(person_details).as_string()
            # server.sendmail(self.settings['from_email'], [to_email], message)
        server.quit()

    def validate_email(self):
        """
        Checks that if the email entered is correct or not using regex
        """
        email = self.settings['from_email']
        if EMAIL_REGEX.match(email) is None:
            print "Entered email is not a valid Email. Please enter proper email"
            exit(1)
        return email


def main():
    print "Welcome to send_greetings........!!!!"
    print "Sending greetings .. . . ."
    greeting = Greeting()
    greeting.send_email()


if __name__ == '__main__':
    main()
