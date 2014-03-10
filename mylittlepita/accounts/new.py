from flask import Blueprint, jsonify, request
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from account import Account 
from mylittlepita.accounts import accounts

@accounts.route('/new', methods=['POST'])
def new_account():
    """
    Endpoint for creating new accounts when the app is installed.
    Returns the account id and the account's secret key.
    """
    if not request.form.get('uuid'):
        return api_error('must provide a device uuid')

    uuid = request.form['uuid'].strip()

    name = request.form['name'].strip() if 'name' in request.form else None
    email = request.form['email'].strip() if 'email' in request.form else None
    phone = request.form['phone'].strip() if 'phone' in request.form else None

    if phone == '':
      phone = None

    if Account.uuid_used(uuid):
        return user_error('an account already exists for this device.')
    if phone and Account.phone_used(phone):
        return user_error('phone number already in use')
    if email and Account.email_used(email):
        return user_error('email already in use')

    new_account = Account.new(uuid, name, phone, email)

    if not new_account:
        return api_error('unable to create new account')

    ret = {'aid': new_account.aid, 'key': new_account.key}
    return jsonify(**ret)

