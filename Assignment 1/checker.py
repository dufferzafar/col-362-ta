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

* Extract all Created Views, so that we can later drop them

Suggestions for doc:

* Remove cleanup section?
    * We'll do cleanup ourself?
"""


import sys
import os
import re


numQ = 22

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

    for l in flines[1:]:

        m = re.match(r"--(\d+)--", l)
        if m:
            q = m.group(1)
            print(l, q)

    if list(sorted(parts.keys())) != ["PREAMBLE"] + list(range(1,numQ+1)):
        err(
            "Not all parts are present.\n"
            "Make sure you create sections for each question, even if you leave them empty."
        )

if __name__ == "__main__":

    main(sys.argv[1])
