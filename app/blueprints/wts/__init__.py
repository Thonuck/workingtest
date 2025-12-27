from flask import Blueprint

bp = Blueprint(
    'wts', 
    __name__,
    template_folder='templates',  # Relativ zu diesem Verzeichnis
    url_prefix='/wts/'
)

from app.blueprints.wts import routes
