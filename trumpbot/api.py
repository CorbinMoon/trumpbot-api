from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from trumpbot.bot import Bot
from trumpbot.db import Query
import datetime


bot = Bot()
app = Flask(__name__)
api = Api(app)


class Chat(Resource):

    def __init__(self):
        self.__query = Query()

    def post(self):
        msg = request.get_json()
        msg['timestamp'] = datetime.datetime.now()
        resp = bot.send(msg)

        self.__query.insert(msg, resp)
        return jsonify(resp)


class Users(Resource):

    def __init__(self):
        self.__query = Query()

    def get(self, user_id):
        msgs = self.__query.select(user_id=user_id)
        return jsonify(msgs)

    def delete(self, user_id):
        self.__query.delete_all(user_id=user_id)
        resp = dict(message='messages successfully deleted')
        return jsonify(resp)


class Msgs(Resource):

    def __init__(self):
        self.__query = Query()

    def delete(self, user_id, msg_id):
        self.__query.delete_by_id(user_id=user_id, id=msg_id)
        resp = dict(message='message successfully deleted')
        return jsonify(resp)


api.add_resource(Chat, '/api/v1/chat')
api.add_resource(Users, '/api/v1/chat/<int:user_id>')
api.add_resource(Msgs, '/api/v1/chat/<int:user_id>/msgs/<int:msg_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            threaded=False)