from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from key import secret_key,salt
import os

app=Flask(__name__)
app.secret_key=secret_key

app.config['SESSION_TYPE']='filesystem'
user=os.environ.get('RDS_USERNAME')
db=os.environ.get('RDS_DB_NAME')
password=os.environ.get('RDS_PASSWORD')
host=os.environ.get('RDS_HOSTNAME')
port=os.environ.get('RDS_PORT')

app.config['UPLOAD_FOLDER'] = '/var/app/current/static/uploads'  # Path to store uploaded files
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    albums = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', albums=albums)


# Route for creating a new album 
@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        album_name = request.form['album_name']
        album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
        os.makedirs(album_path, exist_ok=True)  # Create album directory
        return redirect(url_for('view_album', album_name=album_name))
    return render_template('create_album.html')


# Route for viewing an album
@app.route('/albums/<album_name>')
def view_album(album_name):
    album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
    if not os.path.exists(album_path):
        return redirect(url_for('home'))
    images = []
    for filename in os.listdir(album_path):
        if allowed_file(filename):
            images.append(filename)
    return render_template('view_album.html', album_name=album_name, images=images)


# Route for uploading an image to an album
@app.route('/albums/<album_name>/upload', methods=['GET', 'POST'])
def upload_image(album_name):
    album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
    if not os.path.exists(album_path):
        return redirect(url_for('home'))
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(album_path, filename))
            return redirect(url_for('view_album', album_name=album_name))
    return render_template('upload_image.html', album_name=album_name)


# Route for searching images
@app.route('/search', methods=['GET', 'POST'])
def search_images():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = []
        for album_name in os.listdir(app.config['UPLOAD_FOLDER']):
            album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
            if os.path.isdir(album_path):
                for filename in os.listdir(album_path):
                    if allowed_file(filename) and search_query in filename:
                        results.append((album_name, filename))
        return render_template('search_results.html', search_query=search_query, results=results)
    return render_template('search_images.html')


if __name__ == '__main__':
    app.run()
