from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Album(db.Model):
    __tablename__ = 'album'

    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
