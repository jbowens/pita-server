from flask import Blueprint

accounts = Blueprint('accounts', __name__)

@accounts.route('/new')
def new_account():
    return "LOLOL"
