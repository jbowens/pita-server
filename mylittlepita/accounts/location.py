from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from account import Account
from mylittlepita.accounts import accounts

@accounts.route('/location', methods=['POST'])
def save_location():
    """
    Endpoint for recording a location data point for an account.
    """
    if not g.authorized:
        return access_denied()
    if 'latitude' not in request.form or 'longitude' not in request.form:
        return api_error('latitude and longitude required')
    if request.form['latitude'] == '' or request.form['longitude'] == '':
        return api_error('latitude and longitude required')
    time = request.form['time'] if 'time' in request.form else None

    # If this is the most recent location for the account, update the
    # account's current location.
    if not time or not g.account.loc or time > g.account.loc_time:
        g.account.update_location(request.form['latitude'],
                request.form['longitude'], time)

    return jsonify(status='ok')

