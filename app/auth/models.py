from datetime import datetime, timedelta

from werkzeug.security import check_password_hash

from app import db


class Token(db.Model):
    __tablename__ = 'token'

    token_id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(256), nullable=False)
    valid_to = db.Column(db.DateTime, nullable=False)

    user = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id', ondelete='NO ACTION', onupdate='CASCADE'),
        nullable=False
    )

    def __str__(self):
        return 'Token: {}'.format(self.token_id)

    def __repr__(self):
        return self.__str__()


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
       
    def verify_password(self):
        return check_password_hash(self._password_hash, password)

    def get_token(self):
        token = Token.query.with_parent(self).filter(Token.valid_to <= datetime.now()).first()
        return Token

