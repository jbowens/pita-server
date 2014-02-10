import psycopg2
from flask import Flask, g

app = Flask(__name__)

app.config.from_pyfile('../../config/default.cfg')
app.config.from_envvar('MLP_API_CONFIG_FILE', silent=True)

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

# Spawn the server
if __name__ == '__main__':
    app.run()
