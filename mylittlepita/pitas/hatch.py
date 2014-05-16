from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita.pitas.pita import Pita
from mylittlepita.pitas.event import PitaEvent
from mylittlepita.pitas import pitas

@pitas.route('/hatch', methods=['POST'])
def record_pita_hatch():
    """
    Endpoint used to record that a user has hatched their Pita.
    """
    if not g.authorized:
        return access_denied()

    pita = Pita.get_by_account(g.account.aid)

    if not pita:
        return api_error('That account doesn\'t have a pita.')
    if pita.state != 'egg':
        return api_error('The pita is not in egg form.')

    pita.set_state('alive')
    PitaEvent.record_event(pita, 'born')

    return jsonify(status='ok')
