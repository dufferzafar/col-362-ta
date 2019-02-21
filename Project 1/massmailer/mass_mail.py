import csv
import smtplib
import sys

import sys
sys.path.append("..")
from config import *
from utils import group_IP
from email.mime.text import MIMEText


SUBJECT = "DBMS Project 1 Credentials"


def setup_connection(sender):
    """
    Establish a connection with the smtp server
    """
    smtp = smtplib.SMTP(SMTP_SERVER)
    user = sender["uname"]
    password = sender["pswd"]
    smtp.starttls()
    smtp.login(user, password)
    return smtp


def entry_to_kerberos(e):
    k = e[4:7] + e[2:4] + e[7:]
    return k.lower()


if __name__ == "__main__":
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

            # elif group == "group_0":
            else:
                tolist = [entry_to_kerberos(en) + MAIL_SERVER for en in entry_numbers]

                host = group_IP(group)
                portal_url = host + ":5000"

                body = EMAIL_TEMPLATE.format(
                    uname=group,
                    pswd=CREDENTIALS[group],
                    members=", ".join(names),
                    url=portal_url,
                    host=host
                )

                msg = MIMEText(body)
                msg['Subject'] = SUBJECT
                msg['From'] = SENDER['email']
                msg['To'] = ", ".join(tolist)

                print("Sending Credentials to {}".format(msg['To']))
                print(msg.as_string())
                conn.sendmail(SENDER['email'], tolist, msg.as_string())
