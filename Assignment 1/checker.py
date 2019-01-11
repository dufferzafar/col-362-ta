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
    
    part = "preamble"
    data = flines[0] + "\n"

    # Build parts dict
    for l in flines[1:]:

        if not l:
            continue

        # Since we've already dealt with Preamble
        # A new section is either a question or cleanup
        m = re.match(r"--(\d+|CLEANUP)--", l)
        if m:
            # Save old part
            parts[part] = data
        
            # New part begins
            part = m.group(1).lower()
            data = l + "\n"
        else:
            data += l + "\n"

    # The last part is cleanup
    parts[part] = data

    # Dump parts dict into individual files
    valid_parts = list(map(str, range(1, TOTAL_QUESTIONS + 1)))
    valid_parts += ["preamble", "cleanup"]

    for part in valid_parts:

        if part not in parts:
            err(
                "Not all sections are present.\n"
                "Make sure you create sections for each question, even if you leave them empty."
            )

        with open(str(part)+".sql", "w") as f:
            f.write(parts[part])

        parts.pop(part)

    # Nothing should remain at this point
    if parts:
        err("Extra sections are present. Remove them.")

if __name__ == "__main__":
    main(sys.argv[1])
