"""
Parse PostgreSQL logs to display the queries executed on a DB.

Displays results in a simple HTML table (styled by Bootstrap.)

The page has selections (based on a Dropdown?) for User, DB.

Columns displayed in HTML table: Time, Message
"""

import os
import sys
import csv
import socket

from collections import deque

from flask import Flask, render_template, redirect

import sys
sys.path.append("..")

from config import SERVERS
from utils import my_IP, group_IP

app = Flask(__name__)

# TODO: Add logic to find out which log file to user
PG_DIR = "/var/lib/postgresql/11/main/log/"
PG_LOGs = [f for f in sorted(os.listdir(PG_DIR)) if f.endswith("csv")]

# Pick only the last file
PG_LOG = os.path.join(PG_DIR, PG_LOGs[-1])

# Postgres' csvlog format
# https://github.com/JorgeReus/pg_log_processor/blob/master/pg_log_processor.py#L65
PG_LOG_COLUMNS = [
    'time', 'user', 'database', 'process_id',
    'connection_from', 'session_id', 'session_line_num', 'command_tag',
    'session_start_time', 'virtual_transaction_id', 'transaction_id', 'error_severity',
    'sql_state_code', 'message', 'detail', 'hint', 'internal_query',
    'internal_query_pos', 'context', 'query', 'query_pos', 'location', 'application_name'
]

MAX_ROWS = 25


@app.route("/")
def root():
    return r"Use the /group/{group_number} URL."


@app.route("/group/<int:group_num>")
def index(group_num):

    # Each group is assigned to a specific server
    # So that the load is equally balanced
    # and we only have to read log files present locally on disk
    if my_IP() != group_IP(group_num):
        return redirect("http://%s:%d/group/%d" % (group_IP(group_num), 5001, group_num))

    rows = deque()

    with open(PG_LOG, newline='') as f:
        for row in csv.reader(f):

            # if not row[1].startswith("group_%d" % group_num):
            #     continue

            rows.append([row[0], row[13]])

            if len(rows) > MAX_ROWS:
                rows.popleft()

    return render_template("base.html", rows=reversed(rows), group_num=group_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
