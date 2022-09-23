from flask import Flask, send_from_directory, Response
import datetime
import os.path
import os
import shutil
# flask --app seducer run --host=0.0.0.0

# TODO:
# make camera dump image and check for eyes every 0.5 seconds at certain endpoint
# 
# last image at /last_image

eyes_output_path = 'static/lasteyes.txt'
images_path = 'static/faces'
known_images_path = 'static/known_faces'
INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS = 3

if not os.path.isdir(known_images_path):
    os.makedirs(known_images_path)

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='web/templates')

def get_file(filename):  # pragma: no cover
    with open(filename, 'r') as f:
        return f.read()

counter = 0

@app.route('/hw')
def hw():
    global counter
    counter += 1
    return f'hello world {counter}'

@app.route('/eyes')
def eyes():
    with open(eyes_output_path, 'r') as f:
        lasteyes = datetime.datetime.fromisoformat(f.read())
    return 'true' if (datetime.datetime.now() - lasteyes).total_seconds() < INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS else 'false'

@app.route('/example')
def example():
    return Response(get_file('example.html'), mimetype="text/html")

@app.route('/v0')
def v0():
    with open(eyes_output_path, 'r') as f:
        lasteyes = datetime.datetime.fromisoformat(f.read())
    if (datetime.datetime.now() - lasteyes).total_seconds() < INTERVAL_TO_SAVE_EYES_IMAGE_SECONDS:
        return Response(get_file('static/sed.html'), mimetype="text/html")
    return Response(get_file('static/first.html'), mimetype="text/html")

@app.route('/annotate/<image>/<name>')
def example(image, name):
    shutil.copyfile(os.path.join(images_path, image), os.path.join(known_images_path, f'{name}.png'))