"""
A flask blueprint for the accounts API. This blueprint handles endpoints
involving creating and interacting with accounts.

@author jbowens
"""
from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from account import Account 

accounts = Blueprint('accounts', __name__)

@accounts.route('/new', methods=['POST'])
def new_account():
    """
    Endpoint for creating new accounts when the app is installed.
    Returns the account id and the account's secret key.
    """
    if ('phone' not in request.form or request.form['phone'] == '') and ('email' not in request.form or request.form['email'] == ''):
        return api_error('phone or email required')
    if 'name' not in request.form or request.form['name'] == '':
        return api_error('account name is required')
    email = request.form['email'].strip() if 'email' in request.form else None
    phone = request.form['phone'].strip() if 'phone' in request.form else None

    if phone and Account.phone_used(phone):
        return user_error('phone number already in use')
    if email and Account.email_used(email):
        return user_error('email already in use')

    new_account = Account.new(request.form['name'], phone, email)

    if not new_account:
        return api_error('unable to create new account')

    ret = {'aid': new_account.aid, 'key': new_account.key}
    return jsonify(**ret)

@accounts.route('/location', methods=['POST'])
def save_location():
    """
    Endpoint for recording a location data point for an account.
    """
    if not g.authorized:
        return access_denied()
    if 'latitude' not in request.form or 'longitude' not in request.form:
        return api_error('latitude and longitude required')
    time = request.form['time'] if 'time' in request.form else None

    # If this is the most recent location for the account, update the
    # account's current location.
    if not time or not g.account.loc or time > g.account.loc_time:
        g.account.update_location(request.form['latitude'],
                request.form['longitude'], time)
    
    # Record the location
    db = get_db().cursor()
    if time:
        db.execute('INSERT INTO locations (aid, time, loc) VALUES(%s, %s, \'(%s, %s)\')',
                (g.account.aid, time, float(request.form['latitude']), float(request.form['longitude'])))
    else:
        db.execute('INSERT INTO locations (aid, loc) VALUES(%s, \'(%s, %s)\')',
                (g.account.aid, float(request.form['latitude']), float(request.form['longitude'])))
    
    return jsonify(status='ok')

