from trumpbot.bot import bot
from flask import request, jsonify, make_response, abort, session
from flask_restx import Resource, Api
from flask import Flask
from trumpbot.sql import db
from trumpbot import sql
from trumpbot.oauth2 import require_oauth, OAuth2Client, authorization
from trumpbot.utils import hash_password
from werkzeug.security import gen_salt
from werkzeug.exceptions import *
from trumpbot.oauth2 import config_oauth
import os


UPLOADS_DIR = '../static/img'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'trump_key'
app.config['UPLOAD_FOLDER'] = UPLOADS_DIR
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

config_oauth(app)
api = Api(app)


def current_user():
    if 'id' in session:
        uid = session['id']
        return sql.User.query.get(uid)
    return None


@api.route('/clients')
class Clients(Resource):

    def post(self):
        client = OAuth2Client()

        client.client_id = gen_salt(24)
        client.client_secret = gen_salt(48)
        client.client_metadata = request.get_json()

        db.session.add(client)
        db.session.commit()

        return make_response(jsonify({
            "issued_at": client.issued_at,
            "client_id": client.client_id,
            "client_secret": client.client_secret
        }), 201)


@api.route('/oauth2/token')
class Token(Resource):

    def post(self):
        user = current_user()

        if not user:
            username = request.form['username']
            user = sql.User.query.filter_by(username=username).first()
            session['id'] = user.id

        return authorization.create_token_response(request)


@api.route('/chat')
class Chat(Resource):
    method_decorators = [
        require_oauth('profile')
    ]

    def post(self):
        user = current_user()
        msg = request.get_json()

        __msg = sql.Message()
        __msg.user_id = user.id
        __msg.sender = user.username
        __msg.text = msg['text']

        resp = bot.send(msg)

        __resp = sql.Message()
        __resp.user_id = user.id
        __resp.sender = 'Trump Bot'
        __resp.text = resp['text']

        db.session.add(__msg)
        db.session.add(__resp)
        db.session.commit()

        return make_response(jsonify({
            'timestamp': __resp.timestamp,
            'sender': __resp.sender,
            'text': __resp.text
        }), 201)


@api.route('/register')
class Register(Resource):

    def post(self):
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = sql.User.query.filter_by(username=username).first()

        if not user:
            user = sql.User(username=username,
                            email=email,
                            password=hash_password(password))
            db.session.add(user)
            db.session.commit()
            session['id'] = user.id
            return make_response(jsonify({
                'message': 'New user has been created.'
            }), 201)

        abort(409)


@api.route('/chat/<int:user_id>')
class Messages(Resource):
    method_decorators = [
        require_oauth('profile')
    ]

    def get(self, user_id):
        __msgs = []

        msgs = sql.Message.query.filter_by(user_id=user_id).all()

        for msg in msgs:
            __msgs.append({
                'timestamp': msg.timestamp.utcnow(),
                'sender': msg.sender,
                'text': msg.text
            })

        return __msgs

    def delete(self, user_id):

        sql.Message.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({
            'message': 'Message history deleted.'
        })


@api.route('/profile')
class Profile(Resource):
    method_decorators = [
        require_oauth('profile')
    ]

    def get(self):
        user = current_user()

        return jsonify({
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })


####################################################
################## ERROR HANDLERS ##################
####################################################

@app.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad Request'}, 400


@app.errorhandler(401)
def unauthorized(error):
    return {'error': 'Unauthorized',
            'message': 'Invalid credentials.'}, 401


@app.errorhandler(403)
def forbidden(error):
    return {'error': 'Forbidden'}, 403


@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not Found',
            'message': 'Resource does not exist.'}, 404


@app.errorhandler(405)
def method_not_allowed(error):
    return {'error': 'Method Not Allowed'}, 405


@app.errorhandler(408)
def method_not_allowed(error):
    return {'error': 'Request Timeout',
            'message': 'Request has exceeded the time limit.'}, 408


@app.errorhandler(409)
def conflict(error):
    return {'error': 'Conflict',
            'message': 'Conflict with current state of the server.'}, 409


@app.errorhandler(415)
def unsupported_media_type(error):
    return {'error': 'Unsupported Media Type'}, 415


@app.errorhandler(500)
def server_error(error):
    return {'error': 'Internal Server Error',
            'message': 'Cause is unknown.'}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=80,
            threaded=False)
