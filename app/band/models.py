from flask import url_for
from flask_sqlalchemy import SQLAlchemy

from app import db

from . import band


class Band(db.Model):
    __tablename__ = 'band'

    band_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    year_founded = db.Column(db.SmallInteger, nullable=True)
    year_disbanded = db.Column(db.SmallInteger, nullable=True)
    city = db.Column(db.String(64), nullable=True)
    country = db.Column(db.String(64), nullable=True)

    albums = db.relationship(
        'Album',
        backref=db.backref('albums', lazy=True)
    )

    def get_absolute_url(self):
        return url_for('band.get_band', id=self.band_id)

    def as_dict(self):
        result = {}
        fields = [
            'band_id', 'name', 'year_founded',
            'year_disbanded', 'city', 'country']
        for field in fields:
            result.update({field: getattr(self, field, None)})
        result['self'] = self.get_absolute_url()
        return result

    def __str__(self):
        return "{} {}/{}".format(self.name, self.city, self.country)

    def __repr__(self):
        return self.__str__()

    def set_attrs(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
