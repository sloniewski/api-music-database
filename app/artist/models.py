from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from app import db


class Artist(db.Model):
    __tablename__ = 'artist'

    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    alive = db.Column(db.Boolean, nullable=False, default=True)
    death_date = db.Column(db.Date, nullable=True, default=None)

    def get_absolute_url(self):
        return url_for('artist.get_artist', id=self.artist_id)

    def __str__(self):
        return "{} {}".format(self.name, self.surname)

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        attributes = [
            'name', 'surname', 'birth_date',
            'artist_id', 'alive', 'death_date'
        ]
        result = {}
        for attribute in attributes:
            result[attribute] = getattr(self, attribute, None)
        return result
