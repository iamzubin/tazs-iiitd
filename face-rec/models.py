from app import db


class User(object):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.UnicodeText, unique=True)
    full_name = db.Column(db.UnicodeText)
    faces = db.relationship('Face', backref='user', lazy=True)

    def __init__(self, username, full_name):
        self.username = username
        self.full_name = full_name



class Face(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    face_encoding = db.Column(db.UnicodeText, nullable=False)

    def __init__(self, user_id, face_encoding):
        self.user_id = user_id
        self.face_encoding = face_encoding