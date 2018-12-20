import os
from uuid import uuid4
from io import StringIO

from PIL import Image
import matplotlib.pyplot as plt
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug import secure_filename

from imageparty import throw_party


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), ".")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def resize_and_save_file(fp, path, size=(128, 128)):
    """Take a file object `fp` and save it as an image inder `path`."""
    img = Image.open(fp)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(path)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resize_and_save_file(file, filepath)
            out_path = str(uuid4()) + ".gif"
            img = plt.imread(filepath)
            throw_party(out_path, img)
            return redirect(url_for("party", filename=out_path))

    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/party/<filename>")
def party(filename):
    return render_template(
        "party.html", img_src=url_for("uploaded_file", filename=filename)
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/slack/command", methods=["POST", "HEAD", "OPTIONS"])
def slack_command():
    r = request.json
    return jsonify({"text": "yup"})


if __name__ == "__main__":
    app.run(debug=True)
