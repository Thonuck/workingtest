from flask import Blueprint

bp = Blueprint(
    'exercises',
    __name__,
    template_folder='templates',  # Relativ zu diesem Verzeichnis
    url_prefix='/exercises/'
)

from app.blueprints.exercises import routes
