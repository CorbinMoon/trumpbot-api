from flask import Flask
from flask_restful import Api
from trumpbot.resources import Chat, SignUp
from trumpbot.oauth2 import config_oauth
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

config_oauth(app)
api = Api(app)


# binds resource classes to API endpoints
api.add_resource(SignUp, '/api/v1/sign-up')
api.add_resource(Chat, '/api/v1/chat')


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            threaded=False)