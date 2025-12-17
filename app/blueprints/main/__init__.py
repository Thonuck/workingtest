from flask import Blueprint

bp = Blueprint(
    'main', 
    __name__,
    template_folder='templates',  # Relativ zu diesem Verzeichnis
    url_prefix='/'
)

from app.blueprints.main import routes
