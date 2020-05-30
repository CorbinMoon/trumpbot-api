from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector
from authlib.flask.oauth2.sqla import (
    create_query_client_func,
    create_save_token_func,
    create_revocation_endpoint
)
from authlib.oauth2.rfc6749 import grants
from authlib.specs.rfc6750 import BearerTokenValidator
from .sql import *


class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            return user


class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        token = OAuth2Token.query.filter_by(access_token=token_string).first()
        return token

    def request_invalid(self, request):
        return False

    def token_revoked(self, token):
        return token.revoked


query_client = create_query_client_func(db.session, OAuth2Client)
save_token = create_save_token_func(db.session, OAuth2Token)
authorization = AuthorizationServer(
    query_client=query_client,
    save_token=save_token,
)

require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())


def config_oauth(app):
    # initialize database
    db.init_app(app)
    db.create_all(app=app)

    # initialize authorization server
    authorization.init_app(app)
    authorization.register_grant(grants.ImplicitGrant)
    authorization.register_grant(grants.ClientCredentialsGrant)
    authorization.register_grant(grants.AuthorizationCodeGrant)
    authorization.register_grant(PasswordGrant)

    revocation_cls = create_revocation_endpoint(db.session, OAuth2Token)
    authorization.register_endpoint(revocation_cls)
