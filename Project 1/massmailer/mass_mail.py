import csv
import smtplib
import sys

import sys
sys.path.append("..")
from config import *

SUBJECT = "DBMS Project 1 Credentials"


def setup_connection(sender):
    """
    Establish a connection with the smtp server
    """

    smtp = smtplib.SMTP(SMTP_SERVER)
    # smtp.set_debuglevel(True)
    user = sender["uname"]
    password = sender["pswd"]
    smtp.starttls()
    smtp.login(user, password)
    return smtp


if __name__ == "__main__":
    conn = setup_connection(SENDER)

    with open(RECIPIENTS_FILE) as recepients_file:
        reader = csv.reader(recepients_file)
        for row in reader:
            group = row[0]
            tolist = row[1:]

            if group not in CREDENTIALS:
                print("Credentials for {group} does not exist.".format(group=group))
            else:
                print("Sending Credentials to {}".format(", ".join(tolist)))

                msg = EMAIL_TEMPLATE.format(uname=group, pswd=CREDENTIALS[group])
                msg = "Subject: {}\n\n{}".format(SUBJECT, msg)

                conn.sendmail(SENDER["email"], tolist, msg)
