from app import db

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    question_content = db.Column(db.Text, nullable=False)
    answer_content = db.Column(db.Text, nullable=False)