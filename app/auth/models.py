from flask import url_for

from datetime import datetime, timedelta
from uuid import uuid4

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Token(db.Model):
    __tablename__ = 'token'

    token_id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(256), nullable=False, unique=True)
    valid_to = db.Column(db.DateTime, nullable=False)

    user = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='NO ACTION', onupdate='CASCADE'),
        nullable=False,
    )

    def __str__(self):
        return 'Token: {}'.format(self.token_id)

    def __repr__(self):
        return self.__str__()

    def is_valid(self):
        return self.valid_to >= datetime.now()


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    _password_hash = db.Column(db.String(256), nullable=False)

    tokens = db.relationship(
        'Token',
        backref=db.backref('tokens', lazy=True)
    )

    def __str__(self):
        return '{}'.format(self.username)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def generate_hash(password):
        hash = generate_password_hash(
            password=password,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        return hash

    def set_password(self, password):
        self._password_hash = self.generate_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def get_token(self, days_valid=30):
        token = Token.query.with_parent(self).filter(Token.valid_to >= datetime.now()).first()
        if token is None:
            token = Token(
                uuid=str(uuid4()),
                user=self.user_id,
                valid_to=datetime.now() + timedelta(days=days_valid),
            )
            db.session.add(token)
            db.session.commit()
        return token.uuid

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'self': url_for('auth.get_user', id=self.user_id),
        }
