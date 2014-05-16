from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita.pitas.pita import Pita
from mylittlepita.pitas import pitas

@pitas.route('/get', methods=['POST'])
def get_pita():
    """
    Retrieves the Pita associated with the current account, if any.
    """

    # TODO: This should not be a POST endpoint. We can change that later
    # though.

    if not g.authorized:
        return access_denied()

    existing_pita = Pita.get_by_account(g.account.aid)
    if not existing_pita:
        return jsonify(status="ok", has_pita=False)

    pita_dict = vars(existing_pita)
    pita_dict['has_pita'] = True
    pita_dict['status'] = 'ok'
    return jsonify(pita_dict)
