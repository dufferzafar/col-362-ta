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


def entry_to_kerberos(e):
    k = e[4:7] + e[2:4] + e[7:]
    return k.lower()


if __name__ == "__main__":
    IITD = "@iitd.ac.in"
    PORTAL_URL = "nothing"
    conn = setup_connection(SENDER)

    with open(RECIPIENTS_FILE) as recepients_file:
        reader = csv.reader(recepients_file)
        next(reader)
        for row in reader:
            group = row[0].strip()
            names = [each.strip() for each in row[1::2] if each.strip()]
            entry_numbers = [each.strip() for each in row[2::2] if each.strip()]

            if group not in CREDENTIALS:
                print("Credentials for {group} does not exist.".format(group=group))
            else:
                tolist = [entry_to_kerberos(en) + IITD for en in entry_numbers]
                print("Sending Credentials to {}".format(", ".join(tolist)))

                msg = EMAIL_TEMPLATE.format(uname=group, pswd=CREDENTIALS[group], members=", ".join(names), url=PORTAL_URL)
                msg = "Subject: {}\n\n{}".format(SUBJECT, msg)

                conn.sendmail(SENDER["email"], tolist, msg)
