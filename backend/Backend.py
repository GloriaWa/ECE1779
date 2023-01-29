import flask as f
import backend.CacheWrapper as Cache
from backend import backendApp

capacity = 16  # Cache initial capacity
cw = Cache.CacheWrapper(capacity)


@backendApp.route('/api/')
def main():
    return f.render_template("main.html")


@backendApp.route('/api/get', methods=['POST'])
def get():
    key = f.request.args.get('key')
    value = cw.get(key)
    if value != -1:
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


'''TODO:
Key is the filename and accordingly file should be the
base64 code from frontend. But how do we transfer the 
code (using args or files or somewhat)?
'''


@backendApp.route('/api/put', methods=['POST'])
def put():
    key = f.request.args.get('key')  # using args to get key
    file = f.request.files.get('files')  # using files to get code
    cw.put(key, file)

    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


@backendApp.route('/api/clear', methods=['POST'])
def clear():
    cw.clear()
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


@backendApp.route('/api/invalidateKey', methods=['POST'])
def invalidateKey():
    key = f.request.args.get('key')
    cw.invalidateKey(key)
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response


@backendApp.route('/api/refreshConfiguration', methods=['POST'])
def refreshConfiguration():
    cap = f.request.args.get('capacity')
    cw.refreshConfigurations(cap)
    response = backendApp.response_class(
        response=f.json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response



@backendApp.route('/api/stats', methods=['GET'])
def currentStats():
    return backendApp.response_class(
        response=f.json.dumps(cw.displayStats()),
        status=200,
        mimetype='application/json'
    )