from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita.pitas.pita import Pita
from mylittlepita.pitas import pitas

@pitas.route('/random', methods=['POST'])
def random_pita():
    """
    An endpoint primarily used for testing. It creates a random
    pita and prints the serialized pita to the user.
    """
    if not g.authorized:
        return access_denied()

    existing_pita = Pita.get_by_account(g.account.aid)
    if existing_pita:
        return api_error('That account already has a pita.')

    random_pita = Pita.create_random_pita(g.account.aid)
    return jsonify(vars(random_pita))
