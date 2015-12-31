import re

EMAIL_REGEX = re.compile("^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,6}$")


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


if __name__ == '__main__':
    main()
