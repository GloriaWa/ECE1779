import flask
from flask import Flask

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

backendApp = Flask(__name__)
backendApp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @backendApp.route('/')
# def main():
#     return flask.render_template("main.html")

from backend import Backend