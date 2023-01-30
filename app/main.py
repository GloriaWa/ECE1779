from flask import render_template, url_for, request, flash
from app import webapp, memcache, localfile
from flask import json
import os,imghdr,base64,magic



@webapp.route('/')
def main():
    return render_template("main.html")





