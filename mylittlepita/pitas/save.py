from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita.pitas.pita import Pita
from mylittlepita.pitas import pitas

@pitas.route('/save', methods=['POST'])
def save_pita():
    """
    Endpoint used to save changes in pita state.
    """
    if not g.authorized:
        return access_denied()

    existing_pita = Pita.get_by_account(g.account.aid)
    if not existing_pita:
        return api_error('That account doesn\'t have a pita.')

    valid_req = True
    valid_req = valid_req and 'happiness' in request.form
    valid_req = valid_req and 'hunger' in request.form
    valid_req = valid_req and 'sleepiness' in request.form

    if not valid_req:
        return api_error('Not all status attributes included in request.')

    existing_pita.save_status({
        'happiness': request.form['happiness'],
        'hunger': request.form['hunger'],
        'sleepiness': request.form['sleepiness']
    })

    return jsonify(status='ok')
