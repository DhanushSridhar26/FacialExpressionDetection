from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import *
import os
import cv2
from flask import Flask, request, redirect, url_for, send_from_directory,render_template

app = Flask(__name__)

app.secret_key="abc"

UPLOAD_FOLDER = 'C:\\Users\\Dhanush\\Desktop\\image'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
   return render_template('index.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            r = cv2.imread(file)
            return redirect(url_for('uploaded_file', filename=filename))	
		
@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('template.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
		


if __name__ == '__main__':
   app.run(host="localhost",port=5000, debu = True)