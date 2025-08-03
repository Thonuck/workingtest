from flask import Blueprint

organizer_bp = Blueprint('organizer', __name__)

from . import routes