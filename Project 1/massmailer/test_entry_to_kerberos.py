"""
Test the Entry number to Kerberos ID function.

Works by converting list of Entry Numbers and looking up in another list of Kerberos IDs.
"""

import csv

def entry_to_kerberos(e):
    k = e[4:7] + e[2:4] + e[7:]
    return k.lower()

KERBEROS_IDS = []
with open('../../Students.csv', newline='') as f:
    for r in csv.reader(f):
        KERBEROS_IDS.append(r[2].strip())


with open('recipients.csv', newline='') as f:
    reader = csv.reader(f)

    # Skip header row!
    next(reader)

    # Skip Shadab's & Harish's row!
    next(reader)

    for r in reader:
        for entry in (r[2], r[4], r[6]):
            entry = entry.strip()
            
            if not entry:
                continue

            kerb = entry_to_kerberos(entry)

            if kerb not in KERBEROS_IDS:
                print("Not Found", entry, kerb)
