from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from authlib.flask.oauth2.sqla import (
    OAuth2ClientMixin,
    OAuth2TokenMixin,
    OAuth2AuthorizationCodeMixin
)
from trumpbot.utils import hash_password


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=True)

    def get_user_id(self):
        return self.id

    def __str__(self):
        return self.username

    def check_password(self, password):
        return self.password == hash_password(password)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )
    timestamp = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )
    text = db.Column(db.String, nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    user = db.relationship('User')



class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )

    user = db.relationship('User')


class OAuth2Client(db.Model, OAuth2ClientMixin):

    id = db.Column(db.Integer, primary_key=True)


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
    )

    user = db.relationship('User')