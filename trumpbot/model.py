from trumpbot.utils import to_model_input, vectorize, process, encode_text
from keras.utils import to_categorical
from keras import models, layers
from keras.optimizers import Adam
from keras.models import model_from_yaml
from textgenrnn import textgenrnn
import json
import pandas as pd


TOPICS_PATH = './trumpbot/models.json'
YML_MODEL_PATH = './data/conf/topics_model.yaml'


class ModelLoader(textgenrnn):

    def __init__(self, weights_path=None,
                 dataset_path=None):
        textgenrnn.__init__(self)
        try:
            self.load(weights_path)
        except OSError:
            self.train_from_file(dataset_path)
            if weights_path is not None:
                self.save(weights_path)

    @staticmethod
    def load_models():
        models = []

        with open(TOPICS_PATH, 'r', encoding='utf-8') as file:
            topics = json.load(file)

        for topic in topics:
            dataset, weights = topic.values()
            models.append(ModelLoader(weights, dataset))

        return models


class RNNTextClassifier:

    def __init__(self):
        self._model = None
        self._vocab = None

    @classmethod
    def _scale_model(cls, num_labels,
                     units,
                     input_shape):

        model = models.Sequential()
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(units=units,
                               input_shape=input_shape,
                               activation='sigmoid'))
        model.add(layers.Dense(units=num_labels,
                               activation='softmax'))
        return model

    def predict_class(self, text):
        input = to_model_input(text, self._vocab)
        return self._model.predict_classes(input)[0]

    def train(self, samples=None,
              labels=None,
              input_shape=(10000,),
              units=100,
              num_labels=16,
              batch_size=128,
              num_epochs=10,
              lr=0.01):

        x_train = vectorize(samples[len(samples) // 2:])
        x_val = vectorize(samples[:len(samples) // 2])
        y_train = to_categorical(labels[len(labels) // 2:])
        y_val = to_categorical(labels[:len(labels) // 2])

        self._model = self._scale_model(
            num_labels=num_labels,
            units=units,
            input_shape=input_shape
        )
        self._model.compile(
            optimizer=Adam(lr=lr),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        self._model.fit(
            x=x_train,
            y=y_train,
            epochs=num_epochs,
            batch_size=batch_size,
            validation_data=(x_val, y_val)
        )

    def load(self, weights_path):
        with open(YML_MODEL_PATH, 'r') as file:
            self._model = model_from_yaml(file.read())
            self._model.load_weights(weights_path)

    def save(self, weights_path):
        with open(YML_MODEL_PATH, 'w+') as file:
            file.write(self._model.to_yaml())
            self._model.save_weights(weights_path)

    def train_from_csv(self, file_path,
                       input_shape=(10000,),
                       units=100,
                       num_labels=16,
                       batch_size=128,
                       num_epochs=10,
                       lr=0.01):

        samples, labels = self.load_csv_data(file_path)

        self.train(samples=samples,
                   labels=labels,
                   input_shape=input_shape,
                   units=units,
                   num_labels=num_labels,
                   batch_size=batch_size,
                   num_epochs=num_epochs,
                   lr=lr)

    def load_csv_data(self, file_path):
        df = pd.read_csv(file_path)
        self._vocab = self.get_vocab(df)

        for i, text in enumerate(df['text']):
            df.at[i, 'text'] = encode_text(text, self._vocab)

        df = df.sample(frac=1)

        samples = df['text'].values.tolist()
        labels = df['label'].values.tolist()

        return samples, labels

    @classmethod
    def get_vocab(cls, df):
        vocab_dict = {}
        text = ' '.join(df['text'].values.tolist())

        for index, word in enumerate(set(process(text))):
            vocab_dict[word] = index

        return vocab_dict

    def save_vocab(self):
        with open('vocab.json', 'w+', encoding='UTF-8') as f:
            json.dump(self._vocab, f)