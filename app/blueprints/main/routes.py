from flask import render_template, jsonify, request, redirect, url_for
from app.blueprints.users import bp
from app import db
from app.models import User

@bp.route('/')
def index():
    users = User.query.all()
    return render_template('main/index.html')
