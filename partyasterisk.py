from __future__ import print_function

import os

from flask import Flask, url_for
import matplotlib.pyplot as plt

from imageparty import throw_party

app = Flask(__name__)


@app.route('/')
def hello():
    img = plt.imread('data/jonathan.png')
    path = 'apitest.gif'
    with open(os.path.join('static', path), 'wb') as out_file:
        throw_party(out_file, img)

    return '<!DOCTYPE html><img src="%s" alt="party hard"/>' % (url_for('static', filename=path))


if __name__ == '__main__':
    app.run(debug=True)
