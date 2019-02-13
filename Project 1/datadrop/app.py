import os
import shutil
import logging

from flask import Flask, render_template, request, make_response
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename

import sys
sys.path.append("..")
from config import CREDENTIALS

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
def hello():
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
        ok = pg_load(user, file_path)
        if ok:
            # TODO: Return data to be displayed in output div
            pass
        else:
            # TODO: Return data to be displayed in error div
            pass

        # TODO: Delete file

    return make_response(("Chunk upload successful", 200))


# TODO: Implement this!
def pg_load(user, dump_path):
    # Decide which host to use based on the user
    # Run the right pg_restore command using subprocess
    # Return data to be displayed in output / error div
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
