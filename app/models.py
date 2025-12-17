from app import db  # ✅ Normaler Import am Anfang!

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
