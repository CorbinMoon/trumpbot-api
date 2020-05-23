from trumpbot.bot import bot
from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from trumpbot.sql import User, db
from trumpbot.validators import validate_password, validate_username
from trumpbot.oauth2 import require_oauth



class Chat(Resource):

    method_decorators = [require_oauth('profile')]

    def post(self):
        msg = request.get_json()
        resp = bot.send(msg)
        return make_response(jsonify(resp), 201)


class SignUp(Resource):

    def post(self):
        username = request.form['username']
        password = request.form['password']

        if not validate_username(username):
            abort(400)

        if not validate_password(password):
            abort(400)

        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username,
                        password=str(hash(password)))
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(message="New user has been created."), 201)

        abort(409)
