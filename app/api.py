
from flask import render_template, url_for, request, flash
from app import webapp, memcache, localfile
from flask import json
import os,imghdr,base64,magic

@webapp.route('/api/delete_all')
def delete_all():
    flag=localfile.clear()
    response = {
        "success": flag
    }
    return json.dumps(response)


@webapp.route('/api/list_keys')
def list_keys():
    response = {
        "success": flag
    }
    return json.dumps(response)
