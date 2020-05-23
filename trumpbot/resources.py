from trumpbot.bot import Bot
from trumpbot.forms import RegistrationForm
from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from trumpbot.sql import User, db

bot = Bot()


class Chat(Resource):

    def post(self):
        msg = request.get_json()
        resp = bot.send(msg)
        return make_response(jsonify(resp), 201)


class SignUp(Resource):

    def post(self):
        form = RegistrationForm(request.form)

        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User(username=form.username.data,
                        password=str(hash(form.password.data)))
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify(message="new user has been created"), 201)

        abort(make_response(
            jsonify(error="username '%s' already exist" % form.username.data),
            409))
