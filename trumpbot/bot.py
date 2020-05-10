from trumpbot.model import RNNTextClassifier, ModelLoader
import datetime


class Bot:

    MODEL_WEIGHTS = '../data/weights/topics.hdf5'

    def __init__(self):
        self._models = ModelLoader.load_models()
        self._rnn_text = RNNTextClassifier()
        self._rnn_text.load(self.MODEL_WEIGHTS)

    def send(self, msg):
        i = self._rnn_text.predict_class(msg['text'])
        text = ' '.join(self._models[i].generate(return_as_list=True))
        resp = dict(user_id=msg['user_id'],
                    timestamp=datetime.datetime.now(),
                    sender="trump",
                    text=text)
        return resp
