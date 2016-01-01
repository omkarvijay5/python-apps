This is a small python script which sends greetings for occassions to list of people through email.

This app got initiated as my father wants to send new year greetings to a bunch of people and he was worried about having a big list. Then i told him that dont worry i will write a script which will automate everything :)

I told him to give me just an email template which he wants to send it to everyone and then a csv file which includes a list of contacts with contact name and email.

Then i thought of making this app more generic so that when he wants to send email for every occassion he just need to change the email template :)

How to use this app?

	1. To have proper from_email and password in settings.txt

	2. To have smtp email settings enabled to your gmail account which can be achieved by turning on https://www.google.com/settings/security/lesssecureapps

	3. list of users in contacts.csv with first_name,last_name,email (comma separated values)

Thats it ...

Now run python send_greetings

The above command will send emails to individual users from csv file with dynamic names from new_year.txt template

Future scope: I am planning to automate this sending email for the whole year. Which means app will remember what are the upcoming occassions of a particular year and sends email to all of them in a given scheduled time, So that i dont have to run the above command for every occassion. I just need to train the app on 31st December with occassions of the coming year :)