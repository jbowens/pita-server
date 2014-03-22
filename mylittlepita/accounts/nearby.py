import datetime
from flask import Blueprint, g, request, jsonify, current_app
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from mylittlepita.accounts import accounts

# The cutoff time at which we no longer consider a collected location
# to be valid.
LOCATION_CUTOFF_TIME = datetime.timedelta(0, 0, 0, 0, 5) # 5 minutes

def get_nearby_accounts():
    cur = get_db().cursor()
    # TODO: Figure out the PostGIS query to retrieve all nearby
    # accounts.
    return []

@accounts.route('/nearby', methods=['GET'])
def nearby_accounts():
    """
    Retrieves information about nearby accounts, including their
    pitas.
    """
    if not g.authorized:
        return access_denied()

    # TODO: If latitude and longitude GET parameters were provided,
    # update the account's current location.

    if not g.account.loc or not g.account.loc_time:
        return api_error('there is no location for the current account')

    cur_time = datetime.datetime.now()
    if g.account.loc_time + LOCATION_CUTOFF_TIME < cur_time:
        # The most recent location we have for this account is
        # too old to use for finding nearby accounts.
        return api_error('the current account location is too stale for that')

    nearby_accounts = get_nearby_accounts()

    # TODO: Figure out the format in which we want to send back nearby
    # accounts and pitas. We need to be careful to not give too much
    # information.

    return jsonify(status='ok')

