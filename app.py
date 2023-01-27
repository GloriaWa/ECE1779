from backend import backendApp


@backendApp.route('/index')
def index():  # put application's code here
    return 'Index Page'

if __name__ == '__main__':
    backendApp.run('0.0.0.0', 1145, debug = True)
