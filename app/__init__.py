# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# 
# db = SQLAlchemy()
# 
# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#     app.config['SECRET_KEY'] = 'dev-secret-key'
#     
#     db.init_app(app)
#     
#     with app.app_context():
#         from app import models
#         
#         # Blueprints registrieren
#         from app.blueprints.users import bp as users_bp
#         from app.blueprints.main import bp as main_bp
#         # from app.blueprints.posts import bp as posts_bp
#         # from app.blueprints.auth import bp as auth_bp
#         
#         app.register_blueprint(users_bp)
#         app.register_blueprint(posts_bp)
#         app.register_blueprint(auth_bp)
#         
#         db.create_all()
#     
#     return app



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 1. db-Instanz erstellen (ohne App)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # TODO: Use environment variable for production: os.environ.get('SECRET_KEY')
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # 2. db mit App verbinden
    db.init_app(app)
    
    # 3. Blueprints registrieren (INNERHALB create_app)
    with app.app_context():
        from app import models

        from app.blueprints.users import bp as users_bp
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(users_bp)
        app.register_blueprint(main_bp)
        
        db.create_all()
    
    return app
