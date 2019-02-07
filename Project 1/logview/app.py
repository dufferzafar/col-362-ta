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

from config import SERVERS

app = Flask(__name__)

# TODO: Add logic to find out which log file to user
# PG_DIR = "/var/lib/postgresql/11/main/log/"
# PG_LOG = PG_DIR + "postgresql-2019-01-28_184545.csv"
PG_LOG = "/home/dufferzafar/dev/ta-iitd/spring-2019 - COL 362 - 632/Project 1/logview/postgresql-2019-01-28_184545.csv"

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


def get_IP():
    """
    Returns primary IP address

    https://stackoverflow.com/a/28950776
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route("/")
def root():
    return r"Use the /group/{group_number} URL."

@app.route("/group/<int:group_num>")
def index(group_num):

    # Each group is assigned to a specific server
    # So that the load is equally balanced
    # and we only have to read log files present locally on disk
    my_IP = get_IP()
    group_IP = list(SERVERS.values())[int(group_num) % 3]
    if my_IP != group_IP:
        return redirect("http://%s:%d" % (group_IP, 5000))

    rows = deque()

    with open(PG_LOG, newline='') as f:
        for row in csv.reader(f):

            # TODO: Filter by current group number
            # if not row[1].startswith("group_%d" % group_num):
            #     continue

            rows.append([row[0], row[13]])
            
            if len(rows) > MAX_ROWS:
                rows.popleft()

    return render_template("base.html", rows=reversed(rows), group_num=group_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)