import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__) #initialize flask
mongo = PyMongo(app) #initialize mongo

client = MongoClient()
db = client.tododb

hashValue = str(uuid.uuid4())

app.config['UPLOAD_FOLDER'] = 'static/uploads' #upload directory
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #valid extensions

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    print("/")
    online_users = mongo.db.users.find({'online': True})
    BASE_DIR = 'static'
    abs_path = os.path.join(BASE_DIR, 'uploads')
    path = "uploads"
    files = os.listdir(abs_path)
    return render_template('index.html', files=files, path=path, online_users=online_users)


# Route that will process the file upload
@app.route('/uploads', methods=['POST'])
def upload():
    print("/uploads - start")
    #hashValue = str(uuid.uuid4())
    uploadFolder = app.config['UPLOAD_FOLDER']
    os.mkdir(str(uploadFolder)+"/"+str(hashValue))

    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    print(request.files.getlist("file[]"))
    filenames = []
    i=0
    for file in uploaded_files:
        print(str(file) +" "+ str(i))
        # Check if the file is one of the allowed types/extensions
        if file:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
                # Move the file form the temporal folder to the upload
                # folder we setup
            file.save(os.path.join(str(uploadFolder)+"/"+str(hashValue), filename))
                # Save the filename into a list, we'll use it later
            filenames.append(filename)
            print(filename)
            i+=1
                # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file

    print("/uploads - end")
    return render_template('upload.html', filenames=filenames, hashValue = hashValue, uploadFolder = str(uploadFolder))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("/uploaded_file")
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/new', methods=['POST'])
def new():
    item_doc = {
        '_id': hashValue,
        'name':request.form['name'],
        'description': request.form['description']
    }
    db.tododb.insert_one(item_doc)
    #find = db.tododb.find(request.form['name'])
    #print(find)
    _items = db.tododb.find()
    print(_items)
    items = [item for item in _items]
    return render_template('new.html',items=items)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("80"),
        debug=True
    )
