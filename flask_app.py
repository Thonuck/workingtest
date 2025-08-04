# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, redirect, url_for
from models import db
from blueprints.main.routes import main_bp
from blueprints.organizer.routes import organizer_bp
from blueprints.helper.routes import helper_bp
from config import Config
from extensions import init_extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(organizer_bp, url_prefix='/organizer')
    app.register_blueprint(helper_bp, url_prefix='/helper')

    return app

app = create_app()



if __name__ == '__main__':
    app.run(debug=True)