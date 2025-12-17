from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 1. db-Instanz erstellen (ohne App)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    # 2. db mit App verbinden
    db.init_app(app)
    
    # 3. Blueprints registrieren (INNERHALB create_app)
    with app.app_context():
        from app.blueprints import users  # Import hier!
        app.register_blueprint(users.bp)
        
        db.create_all()
    
    return app
