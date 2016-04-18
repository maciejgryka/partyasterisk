from __future__ import print_function

import os
from uuid import uuid4

import matplotlib.pyplot as plt
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from werkzeug import secure_filename

from imageparty import throw_party


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg',])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img = plt.imread(filepath)
            out_path = str(uuid4()) + '.gif'
            with open(os.path.join(app.config['UPLOAD_FOLDER'], out_path), 'wb') as out_file:
                throw_party(out_file, img)
            return redirect(url_for('uploaded_file', filename=out_path))

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
