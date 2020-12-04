import base64
import io
import os

import PIL.Image
from flask_bootstrap import Bootstrap
from flask import Flask
from flask import render_template, request, g, redirect

TEMPLATES_PATH = os.getcwd()

app = Flask(__name__, template_folder='./templates')
bootstrap = Bootstrap(app)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def convert_img2base(filepath):
    im = PIL.Image.open(filepath)

    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    buffer.seek(0)

    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    return data_uri


@app.route('/')
def hello():
    return render_template("success.html",
                           img=convert_img2base(TEMPLATES_PATH + '/templates/icons/logo.png'))


if __name__ == '__main__':
    app.run()
