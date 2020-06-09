from trumpbot.model import RNNTextClassifier, ModelLoader


class Bot:

    MODEL_WEIGHTS = './data/weights/topics.hdf5'

    def __init__(self):
        self._models = ModelLoader.load_models()
        self._rnn_text = RNNTextClassifier()
        self._rnn_text.load(self.MODEL_WEIGHTS)

    def send(self, msg):
        i = self._rnn_text.predict_class(msg['text'])
        text = ' '.join(self._models[i].generate(return_as_list=True))
        return dict(sender="trump", text=text)


bot = Bot()
