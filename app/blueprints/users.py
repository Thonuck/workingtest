from flask import Blueprint, jsonify, request
from app import db              # ✅ Normaler Import am Anfang!
from app.models import User     # ✅ Normaler Import am Anfang!

bp = Blueprint('users', __name__)

@bp.route('/users')
def list_users():
    # Kein Import hier nötig!
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username} for u in users])

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201
