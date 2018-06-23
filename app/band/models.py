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
        for attrib in dir(self):
            if '__' not in attrib:
                value = getattr(self, attrib, '')
                if isinstance(value, (int, str, float)):
                    result.update({attrib: value})
                if isinstance(value, (list)):
                    temp_list = []
                    for x in value:
                        if isinstance(x,(int, str, float)):
                            temp_list.append(x)
                        if isinstance(x,(db.Model)):
                            temp_list.append(str(x))
                    result.update({attrib: temp_list})
        return result

    def __str__(self):
        return "{} {}/{}".format(self.name, self.city, self.country)

    def __repr__(self):
        return self.__str__()
