from flask import Blueprint

bp = Blueprint(
    'users', 
    __name__,
    template_folder='templates',  # Relativ zu diesem Verzeichnis
    url_prefix='/users'
)

from app.blueprints.users import routes
