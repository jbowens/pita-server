import psycopg2, os
from flask import Flask, g, request

app = Flask(__name__,static_folder='tester')

app.config.from_pyfile('../config/default.cfg')
if 'MLP_API_CONFIG_FILE' in os.environ:
    app.config.from_envvar('MLP_API_CONFIG_FILE')

def get_db():
    """
    Opens a new database connection if none exists for the current
    context.
    """
    if not hasattr(g, 'dbconn'):
        db_conn_str = 'dbname=%s user=%s' % (app.config['DATABASE_NAME'],
                                             app.config['DATABASE_USER'])
        g.dbconn = psycopg2.connect(db_conn_str)
        g.dbconn.autocommit = True
    return g.dbconn

@app.teardown_appcontext
def close_db(ctx):
    """
    Closes the database connection if one eixsts for this
    context.
    """
    if hasattr(g, 'dbconn'):
        g.dbconn.close()

@app.before_request
def authorize():
    """
    Check if this is an authorized request. Store the result in the global object. This
    also stores the account if it is an authorized request.
    """
    from accounts import Account
    if 'X-PITA-ACCOUNT-ID' not in request.headers or 'X-PITA-SECRET' not in request.headers:
        g.authorized = False
        g.account = None
    else:
        g.account = Account.get(request.headers['X-PITA-ACCOUNT-ID'],
                                request.headers['X-PITA-SECRET'])
        g.authorized = g.account != None
    if g.authorized:
        g.account.update_last_seen()

@app.route('/')
def show_frontend():
    """
    Simple placeholder if someone tries to hit api.mylittlepita.com
    in their browser.
    """
    if app.debug:
        # If we're in debug mode, let's serve our tester file.
        return app.send_static_file('tester.html')
    else:
        return 'This API is for Pitas only.'

@app.route('/tester/<path:filename>')
def server_tester_resources():
    return app.send_from_directory('tester', filename)

from accounts import accounts
from photos import photos
from pitas import pitas
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(photos, url_prefix='/photos')
app.register_blueprint(pitas, url_prefix='/pitas')

# Spawn the server
if __name__ == '__main__':
    app.run()
