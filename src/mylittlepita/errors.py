from flask import jsonify, request, g
from . import get_db, app

def log_error(error_type, message):
    """
    Logs an error into the database.
    """
    account_id = g.account.aid if g.account else None
    cur = get_db().cursor()
    cur.execute('INSERT INTO errors (type, aid, ip, message) VALUES(%s, %s, %s, %s)',
            (error_type, account_id, request.remote_addr, message))
    cur.close()

def user_error(msg):
    """
    Should be called to return an api error response when the error
    is clearly caused by the user. For example, the user provided
    a phone number that was already in use.
    """
    log_error('user', msg)
    return jsonify(user_error=True, error_message=msg), 400

def api_error(msg):
    """
    Should be called to return a default api error response. This
    should be used when the client is not making valid requests,
    for whatever reason.
    """
    log_error('bad_request', msg)
    return jsonify(user_error=False, error_message=msg), 400

def access_denied():
    """
    Should be called when a request isn't properly authenticated for
    the given action.
    """
    log_error('access_denied', request.path)
    return jsonify(user_error=False, error_message='access denied'), 403

@app.route('/error', methods=['POST'])
def record_error_endpoint():
    """
    An endpoint that allows the client to report errors that occurred on
    the client.
    """
    if 'message' not in request.form:
        return errors.api_error('no error message in call to /error')
    else:
        log_error('client', request.form['message'])
        return jsonify(status='ok')

