from flask import Blueprint, jsonify, request, g

pitas = Blueprint('pitas', __name__)

from random_pita import *
