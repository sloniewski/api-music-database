from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from app import db


class Album(db.Model):
    __tablename__ = 'album'

    album_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    year_released = db.Column(db.SmallInteger, nullable=True)

    band_id = db.Column(
        db.Integer,
        db.ForeignKey('band.band_id', ondelete='NO ACTION',
                      onupdate='CASCADE'),
        nullable=False,
    )

    def get_absolute_url(self):
        return url_for('album.get_album', id=self.album_id)

    def __str__(self):
        return "{} {}".format(self.name, self.year_released)

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        attributes = ['album_id', 'name', 'year_released', 'band_id']
        result = {}
        for attribute in attributes:
            result[attribute] = getattr(self, attribute, None)
        return result
