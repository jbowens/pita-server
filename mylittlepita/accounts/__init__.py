"""
A flask blueprint for the accounts API. This blueprint handles endpoints
involving creating and interacting with accounts.

@author jbowens
"""
from flask import Blueprint, jsonify, request, g
from mylittlepita.errors import api_error, user_error, access_denied
from mylittlepita import get_db
from account import Account 

accounts = Blueprint('accounts', __name__)

from location import save_location
from new import new_account
from nearby import nearby_accounts
