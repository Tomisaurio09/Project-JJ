from extensions import db
import datetime
from datetime import datetime, timezone

class Folder(db.Model):
    __tablename__ = "folders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    notes = db.relationship("Notes", backref="folder", cascade="all, delete-orphan")
