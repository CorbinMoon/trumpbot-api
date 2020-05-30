from flask import Flask
from flask_restful import Api
from trumpbot.resources import Chat, Register, Clients, Token, Messages, Login, Logout
from trumpbot.oauth2 import config_oauth
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'trump_key'.encode('utf-8')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

config_oauth(app)
api = Api(app)


# binds resource classes to API endpoints
api.add_resource(Register, '/api/v1/register')
api.add_resource(Clients, '/api/v1/clients')
api.add_resource(Token, '/api/v1/oauth2/token')
api.add_resource(Login, '/api/v1/login')
api.add_resource(Logout, '/api/v1/logout')
api.add_resource(Chat, '/api/v1/chat')
api.add_resource(Messages, '/api/v1/chat/<int:user_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            threaded=False)