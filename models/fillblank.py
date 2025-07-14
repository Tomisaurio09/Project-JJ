from app import db

class FillBlank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sentence = db.Column(db.String(255), nullable=False)
    hidden_word = db.Column(db.String(100), nullable=False)
