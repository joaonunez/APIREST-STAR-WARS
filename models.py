from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# TABLA: User
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    subscription_date = db.Column(db.DateTime, default=datetime.now, nullable=False)

    favorites = db.relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'subscription_date': self.subscription_date.strftime("%Y-%m-%d %H:%M:%S"),
            'favorites': [favorite.serialize() for favorite in self.favorites]
        }

# TABLA: Planet
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain
        }

# TABLA: Character
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    height = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    gender = db.Column(db.String(10))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight,
            'gender': self.gender
        }

# TABLA: Favorite
class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    user = db.relationship('User', back_populates='favorites')
    planet = db.relationship('Planet')
    character = db.relationship('Character')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet': self.planet.serialize() if self.planet else None,
            'character': self.character.serialize() if self.character else None
        }
