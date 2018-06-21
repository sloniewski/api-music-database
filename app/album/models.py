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
