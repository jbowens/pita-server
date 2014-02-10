"""
A flask blueprint for the accounts API. This blueprint handles endpoints
involving creating and interacting with accounts.

@author jbowens
"""
from flask import Blueprint, jsonify, request
from mylittlepita import get_db, api_error, user_error
from account import Account 

accounts = Blueprint('accounts', __name__)

@accounts.route('/new', methods=['POST'])
def new_account():
    """
    Endpoint for creating new accounts when the app is installed.
    Returns the account id and the account's secret key.
    """
    if 'phone' not in request.form and 'email' not in request.form:
        return api_error('phone or email required')
    if 'name' not in request.form:
        return api_error('account name is required')
    email, phone = request.form['email'].strip(), request.form['phone'].strip()

    if Account.phone_used(phone):
        return user_error('phone number already in use')
    if Account.email_used(email):
        return user_error('email already in use')

    new_account = Account.new(request.form['name'], phone, email)

    if not new_account:
        return api_error('unable to create new account')

    ret = {'aid': new_account.aid, 'key': new_account.key}
    return jsonify(**ret)

