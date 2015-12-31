import re

EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")


class Greeting(object):

    def __init__(self, email):
        self.from_email = email


def get_email():
    while 1:
        email = raw_input("Please Enter your email:")
        if not EMAIL_REGEX.match(email):
            print "Please enter proper email"
        else:
            break
    return email


def main():
    print "Welcome to send_greetings"
    email = get_email()
    greeting = Greeting(email)


if __name__ == '__main__':
    main()
