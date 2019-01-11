#!/usr/bin/env python3

"""
Check whether query.sql file is of right format
Breaks into part-\d+.sql
Create a cleanup.sql

Checks Performed:

* Check whether all sections exist: Preamble, N sections, Cleanup

Requires Parsing:

* Ensure they don't create views inside query sections?
* Ensure they don't use "modification commands" DROP TABLE, INSERT INTO, etc?
    * This doesn't really matter, because the user won't have edit rights anyway.

* Extract all created Views, so that we can drop them later

Suggestions for doc:

* Remove cleanup section?
    * We'll do cleanup ourself?
"""


import sys
import os
import re


TOTAL_QUESTIONS = 22

def err(*msg):
    print(*msg)
    exit(1)

def main(file):

    with open(file) as f:
        fcontents = f.read().strip()

    flines = list(map(lambda l: l.strip(), fcontents.split("\n")))

    if flines[0] != "--PREAMBLE--":
        err("Missing PREAMBLE")
    
    # int -> string
    parts = {}
    data = ""
    Q = 1

    # Build parts dict
    for l in flines[1:]:

        if not l:
            continue

        # Since we've already dealt with Preamble
        # A new section is either a question or cleanup
        if l == "--%d--" % Q:
            if Q == 1:
                parts["preamble"] = data
            else:
                parts[Q-1] = data

            Q += 1
            data = ""

        elif Q == TOTAL_QUESTIONS and l == "--CLEANUP--":
            parts[Q-1] = data
            Q += 1
            data = ""

        else:
            data += l + "\n"

    # The last part is cleanup
    parts["cleanup"] = data

    # Dump parts dict into individual files
    for part in range(1, TOTAL_QUESTIONS + 1) + ["preamble", "cleanup"]:

        if part not in parts:
            err(
                "Not all parts are present.\n"
                "Make sure you create sections for each question, even if you leave them empty."
            )

        with open(str(part)+".sql", "w") as f:
            f.write(data)

if __name__ == "__main__":
    main(sys.argv[1])
