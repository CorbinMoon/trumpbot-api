from trumpbot.bot import bot
from flask import request, jsonify, make_response, abort, session, redirect
from flask_restful import Resource
from trumpbot.sql import User, db, Message
from trumpbot.oauth2 import require_oauth, OAuth2Client, authorization
from trumpbot.utils import hash_password, parse_basic_auth_header
from werkzeug.security import gen_salt


def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return redirect('/api/v1/login')


class Clients(Resource):

    def post(self):

        user = current_user()
        client = OAuth2Client()

        client.client_id = gen_salt(24)
        client.client_secret = gen_salt(48)
        client.user_id = user.id
        client.client_metadata = request.get_json()

        db.session.add(client)
        db.session.commit()

        client_response = {
            "issued_at": client.issued_at,
            "client_id": client.client_id,
            "client_secret": client.client_secret
        }

        return make_response(jsonify(client_response), 201)


class Token(Resource):

    def post(self):
        return authorization.create_token_response(request)


class Chat(Resource):

    method_decorators = [
        require_oauth('profile')
    ]

    def post(self):
        user = current_user()

        msg = request.get_json()

        __msg = Message()
        __msg.user_id = user.id
        __msg.sender = user.username
        __msg.text = msg['text']

        resp = bot.send(msg)

        __resp = Message()
        __resp.user_id = user.id
        __resp.sender = 'trump'
        __resp.text = resp['text']

        db.session.add(__msg)
        db.session.add(__resp)
        db.session.commit()

        return make_response(jsonify(__resp.msg), 201)


class Register(Resource):

    def post(self):
        basic_auth = request.headers.get('Authorization')
        username, password = parse_basic_auth_header(basic_auth)

        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username=username,
                        password=hash_password(password))
            db.session.add(user)
            db.session.commit()
            session['id'] = user.id
            return make_response(jsonify(message="New user has been created."), 201)

        abort(409)


class Logout(Resource):

    def get(self):
        del session['id']
        return jsonify(dict(message="Successfully logged out."))


class Login(Resource):

    def post(self):

        basic_auth = request.headers.get('Authorization')
        username, password = parse_basic_auth_header(basic_auth)

        user = User.query.filter_by(username=username).first()

        if not user:
            abort(400)

        if user.check_password(password):
            session['id'] = user.id
            return jsonify(dict(message="Login Successful."))

        abort(401)


class Messages(Resource):

    method_decorators = [
        require_oauth('profile')
    ]

    def get(self, user_id):
        __msgs = []

        msgs = Message.query.filter_by(user_id=user_id).all()

        for msg in msgs:
            __msgs.append(msg.msg)

        return jsonify(__msgs)
