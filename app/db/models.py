from gino import Gino
from datetime import datetime
from sqlalchemy import Enum

db = Gino()

class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

class Sport(db.Model, TimestampMixin):
    __tablename__ = "sports"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)

