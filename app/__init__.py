from flask import Flask

global memcache

webapp = Flask(__name__)
webapp.secret_key = 'random_key'
localfile = {}
memcache={}

from app import main, frontend_html, api




