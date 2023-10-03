from gino import Gino
from datetime import datetime
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum

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

class EventType(Enum):
    PREPLAY = "preplay"
    INPLAY = "inplay"

class EventStatus(Enum):
    PENDING = "pending"
    STARTED = "started"
    ENDED = "ended"
    CANCELLED = "cancelled"

class Event(db.Model, TimestampMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), nullable=False, unique=True)
    active = db.Column(db.Boolean(), default=True)
    type = db.Column(SQLAlchemyEnum(EventType), nullable=False)
    sport_id = db.Column(db.Integer(), db.ForeignKey('sports.id'), nullable=False)
    status = db.Column(SQLAlchemyEnum(EventStatus), nullable=False)
    scheduled_start = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    actual_start = db.Column(db.DateTime())

class SelectionOutcome(Enum):
    UNSETTLED = "unsettled"
    VOID = "void"
    LOSE = "lose"
    WIN = "win"

class Selection(db.Model, TimestampMixin):
    __tablename__ = "selections"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    outcome = db.Column(SQLAlchemyEnum(SelectionOutcome), nullable=False)

