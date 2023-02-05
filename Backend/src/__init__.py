import flask
from flask import Flask

UPLOAD_FOLDER = ''

backendApp = Flask(__name__)
backendApp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @backendApp.route('/')
# def main():
#     return flask.render_template("main.html")

from Backend.src import Backend