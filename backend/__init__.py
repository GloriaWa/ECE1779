import flask
from flask import Flask

backendApp = Flask(__name__)

# @backendApp.route('/')
# def main():
#     return flask.render_template("main.html")

from backend import Backend