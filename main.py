from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import *
import os
import cv2
from flask import Flask, request, redirect, url_for, send_from_directory,render_template
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras import utils
from tensorflow.keras import layers
from tensorflow import keras
import cv2
app = Flask(__name__)

app.secret_key="abc"

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

model = keras.models.load_model('model.h5')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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
            fff=os.getcwd()+"\\static\\image"
            file.save(os.path.join(fff, filename))
            return redirect(url_for('uploaded_file', filename=filename))	
		
@app.route('/show/<filename>')
def uploaded_file(filename):
	print(filename)
	return render_template('template.html', filename=filename)

@app.route('/uploads/<filename>')
def sefile(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/predict/<filename>')
def predict(filename):
	fff=os.getcwd()+"\\static\\image\\"+filename
	img = cv2.imread(fff,0)

	faces = face_cascade.detectMultiScale(img, 1.3, 5)

	x1=faces[0][0]
	y1=faces[0][1]
	x2=x1+faces[0][2]
	y2=y1+faces[0][3]

	y=cv2.resize(img[y1:y2,x1:x2],(48,48))
	y=y.reshape(1,48,48,1)

	k = model.predict_classes(y)
	l = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

	data = l[k[0]]
	print(data)
	return render_template("template.html" , data=data) 


