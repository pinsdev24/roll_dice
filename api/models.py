from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, created_at)-> None:
        self.name = name
        self.created_at = created_at

    def serialize(self):
        date = ""
        if self.created_at:
            date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return {
            'id': self.id,
            'name': self.name,
            'created_at': date
        }

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    creator_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    players = db.relationship('Player', secondary='session_players', backref=db.backref('sessions', lazy=True))

    def __init__(self, start_date, end_date, creator_id)-> None:
        self.start_date = start_date
        self.end_date = end_date
        self.creator_id = creator_id

    def serialize(self):
        start = ""
        end = ""
        if self.start_date:
            start = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
        if self.end_date:
            end = self.end_date.strftime('%Y-%m-%d %H:%M:%S')
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'start_date': start,
            'end_date': end
        }

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    score = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    def __init__(self, start_date, end_date, score, session_id, player_id)-> None:
        self.start_date = start_date
        self.end_date = end_date
        self.score = score
        self.session_id = session_id
        self.player_id = player_id

    def serialize(self):
        start = ""
        end = ""
        if self.start_date:
            start = self.start_date.strftime('%Y-%m-%d %H:%M:%S')
        if self.end_date:
            end = self.end_date.strftime('%Y-%m-%d %H:%M:%S')
        return {
            'id': self.id,
            'session_id': self.session_id,
            'player_id': self.player_id,
            'score': self.score,
            'start_date': start,
            'end_date': end
        }

session_players = db.Table('session_players',
    db.Column('session_id', db.Integer, db.ForeignKey('session.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    default_dice_count = db.Column(db.Integer, nullable=False)
    max_games_per_session = db.Column(db.Integer, nullable=False)
    max_sessions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, default_dice_count, max_games_per_session, max_sessions, created_at, updated_at)-> None:
        self.default_dice_count = default_dice_count
        self.max_games_per_session = max_games_per_session
        self.max_sessions = max_sessions
        self.updated_at = updated_at
        self.created_at = created_at

    def serialize(self):
        return {
            'id': self.id,
            'default_dice_count': self.default_dice_count,
            'max_games_per_session': self.max_games_per_session,
            'max_sessions': self.max_sessions,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }