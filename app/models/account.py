from app import app, db


class Account(db.Model):
    """class for instagram account"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))