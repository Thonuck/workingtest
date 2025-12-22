from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1. db-Instanz erstellen (ohne App)
db = SQLAlchemy()



def create_app(config=None):
    app = Flask(__name__)
    if config is None:
        app.config['SECRET_KEY'] = 'your_secret_key_here_change_in_production'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    else:
        app.config.update(config)

    # 2. db mit App verbinden
    db.init_app(app)
    
    # LoginManager initialisieren und user_loader registrieren (außerhalb des App-Kontexts)
    login_manager = LoginManager(app)
    login_manager.login_view = 'users.login'

    from app import models

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    # 3. Blueprints registrieren (INNERHALB create_app)
    with app.app_context():
        from app.blueprints.users import bp as users_bp
        from app.blueprints.main import bp as main_bp
        app.register_blueprint(users_bp)
        app.register_blueprint(main_bp)
        
        db.create_all()

        try:
            existing_user = models.User.query.filter_by(username="admin").first()

            if existing_user:
                print("User existiert bereits!")
            else:
                admin_user = models.User(username="admin", role="admin")
                admin_user.set_password("admin")
                db.session.add(admin_user)
                db.session.commit()
        except Exception as e:
            print(f"Hinweis: Admin-User konnte nicht erstellt werden: {e}")
            print("Falls Schema-Fehler: Bitte reset_database.py ausführen")
    
    return app
