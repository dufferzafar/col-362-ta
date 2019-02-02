CREDENTIALS = {
    "admin": "This is a long passphrase that no one can guess.",

    # Passwords for 40 groups of students
    "group_1": "444264",
    "group_2": "705246",
    "group_3": "280496",
    "group_4": "972481",
    "group_5": "373775",
    "group_6": "148752",
    "group_7": "351762",
    "group_8": "424647",
    "group_9": "918736",
    "group_10": "755908",
    "group_11": "210231",
    "group_12": "491353",
    "group_13": "273104",
    "group_14": "375843",
    "group_15": "645646",
    "group_16": "993365",
    "group_17": "735144",
    "group_18": "488448",
    "group_19": "967364",
    "group_20": "360767",
    "group_21": "401615",
    "group_22": "872799",
    "group_23": "741574",
    "group_24": "128064",
    "group_25": "660393",
    "group_26": "278580",
    "group_27": "759267",
    "group_28": "152638",
    "group_29": "403650",
    "group_30": "837565",
    "group_31": "804993",
    "group_32": "387102",
    "group_33": "185922",
    "group_34": "149854",
    "group_35": "899943",
    "group_36": "448939",
    "group_37": "543166",
    "group_38": "939257",
    "group_39": "341821",
    "group_40": "383543",
}

if __name__ == "__main__":
    # All passwords should be unique
    assert(len(set(CREDENTIALS.values())) == len(CREDENTIALS))

    # And must have a length of atleast 6 chars
    assert(all(len(v) >= 6 for v in CREDENTIALS.values()))
