import flask as f
import Backend.src.CacheWrapper as Cache

from Backend.src import backendApp
from flask import jsonify
from Frontend.Utilities import get_cache_parameter, set_status

capacity = 12  # Cache initial capacity
# 'LUR' is the initial strategy

cw = Cache.CacheWrapper(capacity)

@backendApp.route('/get', methods=['POST'])
def get():

    js = f.request.get_json(force=True)
    key = js["key"]
    value = cw.get(key)

    if value != -1:
        message = "hit"
        return jsonify({"ikey": key,
                        "img": value,
                        "message": message
                        })
    else:
        message = "miss"
        return jsonify({"ikey": "",
                        "img": "",
                        "message": message
                        })

@backendApp.route('/put', methods=['POST'])
def put():
    js = f.request.get_json(force=True)
    key = js["key"]
    img = js["img"]
    cw.put(key, img)

    message = "ok"
    return jsonify({
                    "message": message
                    })

@backendApp.route('/clear', methods=['POST'])
def clear():
    cw.clear()

    message = "ok"
    return jsonify({
        "message": message
    })

@backendApp.route('/invalidate', methods=['POST'])
def invalidateKey():

    js = f.request.get_json(force=True)
    cw.invalidate(js["key"])

    message = "ok"
    return jsonify({
        "message": message
    })

@backendApp.route('/get_key_list', methods=['POST'])
def getKeyList():

    count = len(cw.memcache)

    li = []
    for key in cw.memcache:
        li.append(key)

    message = "success"
    return jsonify({"count": count,
                    "keyList": li,
                    "message": message
                    })

@backendApp.route('/refreshConfiguration', methods=['POST'])
def refreshConfiguration():
    cache_params = get_cache_parameter()

    cap = cache_params[2]
    replace = cache_params[3]

    cw.refreshConfigurations(cap, replace)
    message = "ok"
    return jsonify({
        "message": message
    })

@backendApp.route('/stats', methods=['POST'])
def heartBeatStatus():
    item_count = len(cw.memcache)
    request_count = cw.accessCount
    miss_count = cw.accessCount - cw.hit
    size = cw.getSize()

    set_status(size, item_count, request_count, miss_count)
    message = "ok"
    return jsonify({
        "message": message
    })

