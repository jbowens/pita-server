import datetime
from flask import Blueprint, g, request, jsonify, current_app
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from mylittlepita.accounts import accounts
from psycopg2.extras import RealDictCursor

# The cutoff time at which we no longer consider a collected location
# to be valid.
LOCATION_CUTOFF_TIME = datetime.timedelta(0, 0, 0, 0, 5) # 5 minutes

def get_nearby_accounts():
    cur = get_db().cursor(cursor_factory = RealDictCursor)
    cur.execute('SELECT accounts.*, ST_Distance_Sphere(ST_SetSRID(ST_MakePoint(%s,%s),4326),accounts.loc) AS dist_meters FROM accounts WHERE loc_time > now() - interval \'5 minutes\' ORDER BY accounts.loc <-> ST_SetSRID(ST_MakePoint(%s,%s),4326) LIMIT 25', (g.account.latitude, g.account.longitude, g.account.latitude, g.account.longitude))
    accounts = cur.fetchall()
    return accounts

@accounts.route('/nearby', methods=['POST'])
def nearby_accounts():
    """
    Retrieves information about nearby accounts, including their
    pitas.
    """
    if not g.authorized:
        return access_denied()

    if request.form.get('latitude') and request.form.get('longitude'):
        # The latitude and longitude parameters were provided, so
        # we should update the account's current location.
        g.account.update_location(request.form.get('latitude'),
                                  request.form.get('longitude'),
                                  None)

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
    output = []
    for acc in nearby_accounts:
        if acc['aid'] != g.account.aid:
            acc_output = dict()
            acc_output['aid'] = acc['aid']
            # acc_output['dist'] = acc['dist_meters']
            output.append(acc_output)

    current_app.logger.debug(output)

    return jsonify(nearby_accounts=output)

