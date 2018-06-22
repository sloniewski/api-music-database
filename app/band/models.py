from flask_sqlalchemy import SQLAlchemy

from app import db


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
    
    def __str__(self):
        return "{} {}/{}".format(self.name, self.city, self.country)
