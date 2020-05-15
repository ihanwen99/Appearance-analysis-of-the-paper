from __future__ import unicode_literals

import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['DROPZONE_REDIRECT_VIEW'] = 'hello'  # set redirect view
app.config['DROPZONE_REDIRECT_VIEW'] = 'result'  # function-name (not the true url)
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pdf'

dropzone = Dropzone(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print("<---The uploaded file is {}.--->".format(file.filename))
            filename = "upload.pdf"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            return redirect(url_for('process'))
    return render_template('upload.html')


@app.route('/process')
def process():
    print("<---Processing...--->")
    print("<---1+1= ======= 2--->")
    return "This will do nothing, and it can be changed to anything"


# Hello Page -> hello.html
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return render_template('hello.html')


@app.route('/apperance-analysis', methods=['GET', 'POST'])
def result():
    return render_template('result.html')


@app.route('/main', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
