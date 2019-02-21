
SERVERS = {
    "vpl1": "10.17.50.247",
    "vpl2": "10.17.50.115",
    "vpl3": "10.17.51.19",
}

MAIL_SERVER = "@iitd.ac.in"

###########################################################################

SENDER = {
    "email": "",
    "uname": "",
    "pswd": "",
}

SMTP_SERVER = ""

RECIPIENTS_FILE = "recipients.csv"

EMAIL_TEMPLATE = """
Hi,

Your group members are: {members}

Use the following username and password to upload your database to the portal.

Uername: {uname}
Password: {pswd}

Portal's URL: http://{url}/
(will only work when connected to IIT Delhi's network)

Use the aforementioned credentials to connect to this DB:

Host: {host}
Port: 5432
Database Name: {uname}

Regards,
Shadab & Harish
"""

###########################################################################

CREDENTIALS = {
    # Admin account
    "test_0": "test",
    "group_0": "This is a long passphrase that no one can guess.",

    # Passwords for 40 groups of students
    "group_1": "283-216-380",
    "group_2": "534-643-377",
    "group_3": "202-901-602",
    "group_4": "117-958-344",
    "group_5": "862-807-778",
    "group_6": "529-739-414",
    "group_7": "214-658-874",
    "group_8": "198-929-696",
    "group_9": "902-824-299",
    "group_10": "815-685-329",
    "group_11": "191-574-834",
    "group_12": "872-725-884",
    "group_13": "205-265-669",
    "group_14": "413-542-586",
    "group_15": "215-952-732",
    "group_16": "316-430-547",
    "group_17": "413-746-464",
    "group_18": "604-287-987",
    "group_19": "411-306-727",
    "group_20": "670-176-755",
    "group_21": "885-479-849",
    "group_22": "732-722-568",
    "group_23": "115-931-519",
    "group_24": "456-932-282",
    "group_25": "887-323-760",
    "group_26": "232-820-678",
    "group_27": "455-749-988",
    "group_28": "257-639-469",
    "group_29": "923-594-533",
    "group_30": "776-302-579",
    "group_31": "235-563-714",
    "group_32": "462-702-921",
    "group_33": "880-609-721",
    "group_34": "141-677-925",
    "group_35": "860-588-775",
    "group_36": "787-867-421",
    "group_37": "491-502-391",
    "group_38": "405-385-140",
    "group_39": "661-665-963",
    "group_40": "380-866-539",
}

if __name__ == "__main__":
    # All passwords should be unique
    assert(len(set(CREDENTIALS.values())) == len(CREDENTIALS))
