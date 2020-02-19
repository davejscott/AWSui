"""
Created on March 2018


@author: 
	Invenio


"""

#################################################################################################################################################




"""

Prerequisites

    Gensim
    Numpy==1.11.3
    Pandas
    Sklearn
    Dash
    Antiwords
    autocorrect



"""

import glob
import os
import warnings
import textract
import requests
from flask import (Flask,session, g, json, Blueprint,flash, jsonify, redirect, render_template, request,
                   url_for, send_from_directory)
from gensim.summarization import summarize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from werkzeug.utils import secure_filename

import pdf2txt as pdf
import PyPDF2

#import screen
import search
import hashlib

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

app = Flask(__name__)

app.config.from_object(__name__) # load config from this file , flaskr.py

#define APP_ROOT for complete.html (saving pdfs)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Load default config and override config from an environment variable
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='7b4d7a208a333b46acdc9da159e5be7a',
    SECRET_KEY='development key',
))


app.config['UPLOAD_FOLDER'] = 'Original_Resumes/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class jd:
    def __init__(self, name):
        self.name = name

def getfilepath(loc):
    temp = str(loc).split('\\')
    return temp[-1]
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif app.config['PASSWORD'] != hashlib.md5(request.form['password'].encode('utf-8')).hexdigest():
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))


@app.route('/')
def home():
    x = []
    for file in glob.glob("./Job_Description/*.txt"):
        res = jd(file)
        x.append(jd(getfilepath(file)))
    print(x)
    return render_template('index.html', results = x)

@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'Original_Resumes/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")  




#@app.route('/results', methods=['GET', 'POST'])
#def res():
#    if request.method == 'POST':
#        jobfile = request.form['des']
#        print(jobfile)
#        flask_return = screen.res(jobfile)
        
#        print(flask_return)
#        return render_template('result.html', results = flask_return)



#@app.route('/resultscreen' ,  methods = ['POST', 'GET'])
#def resultscreen():
#    if request.method == 'POST':
#        jobfile = request.form.get('Name')
#        print(jobfile)
#        flask_return = screen.res(jobfile)
#        return render_template('result.html', results = flask_return)



@app.route('/resultsearch' ,methods = ['POST', 'GET'])
def resultsearch():
    if request.method == 'POST':
        search_st = request.form.get('Name')
        print(search_st)
    result = search.res( search_st)
    #return result
    return render_template('result.html', results = result)


@app.route('/Original_Resume/<path:filename>')
def custom_static(filename):
    return send_from_directory('./Original_Resumes', filename)



if __name__ == '__main__':
   # app.run(debug = True) 
    # app.run('127.0.0.1' , 5000 , debug=True)
    #app.run('0.0.0.0' , 5000 , debug=True , threaded=True)
    app.run('0.0.0.0' , 8080 , debug=True)
    
