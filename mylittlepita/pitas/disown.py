from flask import Blueprint, jsonify, g
from mylittlepita.errors import api_error, access_denied
from mylittlepita.pitas import pitas
from mylittlepita.pitas.pita import Pita
from mylittlepita.pitas.event import PitaEvent

@pitas.route('/disown', methods=['POST'])
def record_pita_disown():
    """
    Endpoint used to record that a Pita has been disowned.
    """
    if not g.authorized:
        return access_denied()

    pita = Pita.get_by_account(g.account.aid)

    if not pita:
        return api_error('That account doesn\'t have a pita.')

    if pita.state != 'alive' and pita.state != 'egg':
        return api_error('The pita is not alive.')

    pita.set_state('disowned')
    PitaEvent.record_event(pita, 'disowned')

    return jsonify(status='ok')
