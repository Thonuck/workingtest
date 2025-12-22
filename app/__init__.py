from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1. db-Instanz erstellen (ohne App)
db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    # 2. db mit App verbinden
    db.init_app(app)
    
    # 3. Blueprints registrieren (INNERHALB create_app)
    with app.app_context():

        login_manager = LoginManager(app)
        login_manager.login_view = 'login'

        from app import models
        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))

        from app.blueprints.users import bp as users_bp
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(users_bp)
        app.register_blueprint(main_bp)
        
        db.create_all()

        existing_user = models.User.query.filter_by(name="admin").first()

        if existing_user:
            print("User existiert bereits!")
        else:
            admin_user = models.User(username="admin", rolle="admin")
            admin_user.set_password("admin")
            db.session.add(admin_user)
            db.session.commit()
    
    return app
