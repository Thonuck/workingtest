from flask import Blueprint

bp = Blueprint(
    'starters',
    __name__,
    template_folder='templates',  # Relativ zu diesem Verzeichnis
    url_prefix='/exercises/'
)

from app.blueprints.starters import routes
