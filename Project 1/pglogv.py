"""
Parse PostgreSQL logs to display the queries executed on a DB.

Displays results in a simple HTML table (styled by Bootstrap.)

The page has selections (based on a Dropdown?) for User, DB.

Columns displayed in HTML table: Time, Message
"""

import os
import sys
import csv

from flask import Flask

app = Flask(__name__)

PG_DIR = "/var/lib/postgresql/11/main/log/"

# Postgres' csvlog format
# https://github.com/JorgeReus/pg_log_processor/blob/master/pg_log_processor.py#L65
PG_LOG_COLUMNS = [
    'time', 'user', 'database', 'process_id',
    'connection_from', 'session_id', 'session_line_num', 'command_tag',
    'session_start_time', 'virtual_transaction_id', 'transaction_id', 'error_severity',
    'sql_state_code', 'message', 'detail', 'hint', 'internal_query',
    'internal_query_pos', 'context', 'query', 'query_pos', 'location', 'application_name'
]


@app.route("/")
def index():

    logfile = PG_DIR + "postgresql-2019-01-28_184545.csv"

    rv = ""

    with open(logfile, newline='') as f:
        for row in csv.reader(f):
            # print(row[0])
            rv += row[0] + "<br>"

    return rv


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
