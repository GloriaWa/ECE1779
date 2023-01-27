import flask as f
import backend.CacheWrapper as Cache
from backend import backendApp

capacity = 16 #Cache initial capacity
cw = Cache.CacheWrapper(capacity)


@backendApp.route('/')
def main():
    return f.render_template("main.html")


@backendApp.route('/get', methods=['POST'])
def get():
    key = f.request.args.get('key')
    if key in cw.memcache:
        value = cw.get(key)
        response = backendApp.response_class(
            response=f.json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = backendApp.response_class(
            response=f.json.dumps("Cache Miss"),
            status=400,
            mimetype='application/json'
        )

    return response


@backendApp.route('/put', methods=['POST'])
def put():
    key = f.request.args.get('key')
    value = f.request.args.get('value')
    cw.put(key, value)

    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response

@backendApp.route('/clear', methods=['POST'])
def clear():
    cw.clear()
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response

@backendApp.route('/invalidateKey', methods=['POST'])
def invalidateKey():
    key = f.request.args.get('key')
    cw.invalidateKey(key)
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response

@backendApp.route('/refreshConfiguration', methods=['POST'])
def refreshConfiguration():
    cap = f.request.args.get('capacity')
    cw.refreshConfigurations(cap)
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response