import psycopg2
from flask import Flask, g, jsonify

app = Flask(__name__)

app.config.from_pyfile('../../config/default.cfg')
app.config.from_envvar('MLP_API_CONFIG_FILE', silent=True)

def user_error(msg):
    """
    Should be called to return an api error response when the error
    is clearly caused by the user. For example, the user provided
    a phone number that was already in use.
    """
    # TODO: Logging still might be useful here to see how users
    # are fucking up.
    return jsonify(user_error=True, error_message=msg), 400

def api_error(msg):
    """
    Should be called to return a default api error response. This
    should be used when the client is not making valid requests,
    for whatever reason.
    """
    # TODO: Add logging of API errors. Our iOS client *should* be
    # the only client, so this *should* be indicative of an error
    # in our client. Could also be 1337 haxxors.
    return jsonify(user_error=False, error_message=msg), 400

def get_db():
    """
    Opens a new database connection if none exists for the current
    context.
    """
    if not hasattr(g, 'dbconn'):
        db_conn_str = 'dbname=%s user=%s' % (app.config['DATABASE_NAME'],
                                             app.config['DATABASE_USER'])
        g.dbconn = psycopg2.connect(db_conn_str);
    return g.dbconn

@app.route('/')
def show_frontend():
    """
    Simple placeholder if someone tries to hit api.mylittlepita.com
    in their browser.
    """
    get_db()
    return 'This API is for Pitas only.' 

from accounts import accounts
app.register_blueprint(accounts, url_prefix='/accounts')

# Spawn the server
if __name__ == '__main__':
    app.run()
