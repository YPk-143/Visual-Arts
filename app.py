import shutil
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    albums = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', albums=albums)


@app.route('/create_album', methods=['GET', 'POST'])
def create_album():
    if request.method == 'POST':
        album_name = request.form['album_name']
        album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
        os.makedirs(album_path)
        return redirect(url_for('view_album', album_name=album_name))
    return render_template('create_album.html')


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

# Route for deleting an album
@app.route('/albums/<album_name>/delete', methods=['POST'])
def delete_album(album_name):
    album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
    if not os.path.exists(album_path):
        return redirect(url_for('home'))
    # Delete the album directory and its contents
    shutil.rmtree(album_path)
    return redirect(url_for('home'))
 
# Route for deleting an image from an album
@app.route('/albums/<album_name>/delete_image/<image_name>', methods=['POST'])
def delete_image(album_name, image_name):
    album_path = os.path.join(app.config['UPLOAD_FOLDER'], album_name)
    image_path = os.path.join(album_path, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)
    return redirect(url_for('view_album', album_name=album_name))


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
    app.run(debug=True)
