import os
import uuid
import shutil
import json
import os.path
from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__) #initialize flask
app.config['TEMPLATES_AUTO_RELOAD'] = True

mongo = PyMongo(app) #initialize mongodb
client = MongoClient()
db = client.pysaas

app.config['UPLOAD_FOLDER'] = 'static/uploads' #upload directory
uploadFolder = app.config['UPLOAD_FOLDER']

@app.route('/')
def index():
    print('--> HTTP PAGE: /')
    return render_template('index.html')


@app.route('/storedCases')
def storedCases():
    print('--> HTTP PAGE: /storedCases')
    if (db.pysaas.count() != 0):
        _items = db.pysaas.find()
        items = [item for item in _items]
    else:
        items = 0
    return render_template('storedCases.html',items=items, uploadFolder=uploadFolder)


@app.route('/uploadNew')
def uploadNew():
    print('--> HTTP PAGE: /uploadNew')
    return render_template('uploadNew.html')


@app.route('/uploadDone', methods=['POST','GET'])
def uploadDone():
    hashValue = str(uuid.uuid4()) #create a unique hash (or id)
    os.mkdir(str(uploadFolder)+"/"+str(hashValue)) #make a new folder in static named "uploadFolder"/"hashValue"
    uploaded_files = request.files.getlist("file[]")
    print(request.files.getlist("file[]"))
    filenames = []

    filesJSON = { #JSON to be stored in mongodb
        '_id': hashValue,
        'fileName': '',
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName']
    }

    print("Uploaded files:")
    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(str(uploadFolder)+"/"+str(hashValue), filename))
            filenames.append(filename)

    filesJSON['fileName'] = filenames

    db.pysaas.insert_one(filesJSON) #store the data

    with open(os.path.join(uploadFolder + '/' + hashValue + '/', "data.JSON"), 'w') as outfile:
        json.dump(filesJSON, outfile, ensure_ascii=False)

    return render_template('uploadDone.html', filenames=filenames, hashValue = hashValue, uploadFolder = str(uploadFolder))


@app.route('/static/uploads/<path>', methods=['GET'])
def imageSeek(path):
    print('--> HTTP PAGE: /static/uploads/' + str(path))
    files = os.listdir(os.path.join(uploadFolder, path))
    value = db.pysaas.find_one({"_id":path});
    return render_template('imageSeek.html', files=files, path=path, firstName = value['firstName'],lastName = value['lastName'])


@app.route('/delete/<id>', methods=['POST','GET'])
def delete(id):
    print('--> HTTP PAGE: /delete')
    db.pysaas.delete_one({'_id': id})
    shutil.rmtree((str(uploadFolder)+"/"+str(id)))
    return redirect('/storedCases')


@app.route('/analyze/<hashId>',methods=['POST','GET'])
def analyze(hashId):
    print('--> HTTP PAGE: /analyze/' + str(hashId))
    with open( uploadFolder + '/' + hashId + '/' + 'data.json') as data_file:
        data = json.load(data_file)
    path = '../' + uploadFolder + '/' + hashId +'/'
    return render_template('analyze.html',fileName=json.dumps(data["fileName"]),path=path)


@app.route('/analyze',methods=['GET'])
def redirect1():
    return render_template('analyzeRedirect.html')


@app.route('/analyzeex',methods=['GET'])
def redirect2():
    return render_template('analyzeRedirect2.html')


@app.route('/analyzeex/<hashId>', methods=['POST','GET'])
def analyzeex(hashId):
    print('--> HTTP PAGE: /analyzeex/' + str(hashId))
    with open( uploadFolder + '/' + hashId + '/' + 'data.json') as data_file:
        data = json.load(data_file)
    path = '../' + uploadFolder + '/' + hashId +'/'
    print(path)
    return render_template('analyzeex.html',fileName=json.dumps(data["fileName"]),path=path)


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )


