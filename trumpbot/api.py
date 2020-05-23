from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from trumpbot.bot import Bot
import datetime
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////chat.db'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

api = Api(app)

bot = Bot()


class Chat(Resource):

    def post(self):
        msg = request.get_json()
        msg['timestamp'] = datetime.datetime.now()
        resp = bot.send(msg)

        return make_response(jsonify(resp), 201)


api.add_resource(Chat, '/api/v1/chat')


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            threaded=False)