from flask import render_template, url_for, request
from app import webapp, memcache, localfile
import os,  base64, magic


@webapp.route('/upload')
def redirect_upload():
    return render_template("upload.html")


@webapp.route('/find')
def redirect_find():
    return render_template("find.html")


@webapp.route('/db_config')
def db_config():
    if localfile == {}:
        res = {"no keys":""}
    else:
        res = localfile
    return render_template("db_config.html", all_keys=res)


@webapp.route('/cache_config')
def cache_config():
    if memcache == {}:
        res = ""
    else:
        res = memcache.keys()
    return render_template("cache_config.html", all_keys=res)


@webapp.route('/statistics')
def statistics():
    # log = time activities pair, if not activites, use log=""
    log={"1":"2","3":"4"}
    return render_template("statistics.html",log=log)



@webapp.route('/upload', methods=["POST"])
def upload():
    if request.files['file'].filename == '':
        return render_template("upload.html", msg='No selected file')
    if request.form.get('key') == '':
        return render_template("upload.html", msg='No entered key')

    # save file locally and give path & key to db
    key = request.form.get('key')
    file = request.files['file']
    localfile[key] = os.path.join('app', 'static', file.filename)
    file.save(localfile[key])

    # read as binary and sve content to mem_cache
    f = open(localfile[key], "rb")
    memcache[key] = f.read()
    f.close()
    return render_template("upload.html", msg=file.filename + ' upload success')


@webapp.route('/find', methods=['POST'])
def find():
    key = request.form.get('key')
    if key == '':
        return render_template("find.html", msg="Please enter a key")

    # fetch from memcache
    elif key in memcache:
        mtype = magic.from_buffer(memcache[key], mime=True)
        codedimage = str(base64.b64encode(memcache[key]))[2:-1]
        return render_template("find.html", image="data:" + mtype + ";base64," + codedimage)

    # fetch from db
    elif key in localfile:
        value = localfile[key]
        return render_template("find.html", image=value[4:])

    else:
        return render_template("find.html", msg="Unknown key, Please try again")


@webapp.route('/db_config/clear_keys')
def clear_keys():
    localfile.clear()
    msg = "All keys in database has been cleared"
    return render_template("db_config.html", msg=msg)

@webapp.route('/cache_config/clear_cache')
def clear_cache():
    memcache.clear()
    msg = "All keys in cache has been cleared"
    return render_template("cache_config.html", msg=msg)