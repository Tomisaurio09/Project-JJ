from extensions import db
import datetime
from datetime import datetime, timezone

class Notes(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title  = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey("folders.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))