import os
import psycopg2
import shutil
import logging

from flask import Flask, render_template, request, make_response
from flask_basicauth import BasicAuth
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.utils import secure_filename
import subprocess

import sys
sys.path.append("..")
from config import CREDENTIALS, SERVERS

# TODO: Setup log output?
log = logging.getLogger('datadrop')

app = Flask(__name__)
basic_auth = BasicAuth(app)


def check_creds(user, passw):
    """ Lookup credentials from file. """
    return passw == CREDENTIALS.get(user)


# Use our method instead of the built-in one
basic_auth.check_credentials = check_creds


@app.route('/', methods=['GET', 'POST'])
@basic_auth.required
def index():
    if request.method == 'GET':
        return render_template('base.html')

    # request.method == 'POST'

    file = request.files['file']
    user = request.authorization.username

    # Keep in mind that this function is called multiple times for the same file!
    current_chunk = int(request.form['dzchunkindex'])

    student_dir = os.path.join("../uploads", user)
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)

    file_path = os.path.join(student_dir, secure_filename(file.filename))

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(student_dir) and current_chunk == 0:
        try:
            # Delete the entire student folder
            # Solves the problem of student uploading files with different names
            shutil.rmtree(student_dir)
            os.makedirs(student_dir)
        except OSError:
            return make_response(("Unable to delete old uploads.", 400))

    # Write chunk to file
    try:
        with open(file_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        err = "Couldn't write to file."
        log.exception(err)
        return make_response((err, 500))

    # Finished writing chunks?
    total_chunks = int(request.form['dztotalchunkcount'])
    if current_chunk + 1 == total_chunks:
        msg = pg_load(user, request.authorization.password, file_path)
        
        print(msg)

        # Crude way of detecting that an error has occurred
        if b"ERROR:" in msg:
            print("ERRORR OCCURRED!")
            return make_response((msg, 400))
        else:
            print("No Error!")
            return make_response((msg, 200))

    return make_response(("Chunk upload successful", 200))


def connect(ip, user, pswd, dbname="postgres"):
    print("Connecting to %s:5432" % (ip))
    try:
        conn = psycopg2.connect(
            user=user,
            host=ip,
            port="5432",
            password=pswd,
            dbname=dbname,
        )
        return conn

    except psycopg2.Error as e:
        print("Error connecting to postgres server\n %s" % (str(e)))
        return None


def cleanup(conn, group):
    q1 = "DROP DATABASE IF EXISTS {group};"
    q2 = "CREATE DATABASE {group};"
    conn.autocommit = True
    conn.cursor().execute(q1.format(group=group))
    conn.cursor().execute(q2.format(group=group))
    conn.commit()


def pg_load(user, pswd, dump_path):
    group_no = int(user.split("_")[-1]) % 3 + 1
    key = "vpl" + str(group_no)
    ip = SERVERS[key]

    print("Performing Cleanup before Loading...")
    conn = connect(ip, user, pswd)
    cleanup(conn, user)
    conn.close()

    print("Loading Database")
    cmd = 'PGPASSWORD="{pswd}" psql -h {ip} -d {db} -U {user} < "{dump}"'.format(pswd=pswd, ip=ip, db=user, user=user, dump=dump_path)
    msg = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

    return msg


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
