from flask import Blueprint, jsonify, request, g

pitas = Blueprint('pitas', __name__)

from random_pita import *
from save import *
from get import *
from hatch import *
from death import *
