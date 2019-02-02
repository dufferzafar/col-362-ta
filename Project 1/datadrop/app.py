import os
import logging

from flask import Flask, render_template, request, make_response
from werkzeug.utils import secure_filename

log = logging.getLogger('datadrop')
# TODO: Setup a log output?


app = Flask(__name__)


# TODO: Add Basic Auth


@app.route('/')
def hello():
    return render_template('base.html')


# TODO: Use / route to POST as well?
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    # TODO: Use a different data root than /tmp?
    save_path = os.path.join("/tmp", secure_filename(file.filename))
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if os.path.exists(save_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        # TODO: This needs to be updated?
        return make_response(('File already exists.', 400))

    try:
        with open(save_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())
    except OSError:
        log.exception('Could not write to file.')
        return make_response(("Couldn't write file to disk.", 500))

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
            log.error(f"File {file.filename} was completed, "
                      f"but has a size mismatch."
                      f"Was {os.path.getsize(save_path)} but we"
                      f" expected {request.form['dztotalfilesize']} ")
            return make_response(('Size mismatch', 500))
        else:
            log.info(f'File {file.filename} has been uploaded successfully')
    else:
        log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
                  f'for file {file.filename} complete.')

    return make_response(("Chunk upload successful", 200))

if __name__ == '__main__':
    app.run(debug=True)
