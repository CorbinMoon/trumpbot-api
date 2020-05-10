import string
import numpy as np
from nltk.tokenize import word_tokenize
import json


VOCAB_PATH = './vocab.json'


def vectorize(seqs, dim=10000):
    results = np.zeros(shape=(len(seqs), dim))

    for i, seq in enumerate(seqs):
        results[i, seq] = 1

    return results


def to_model_input(text, vocab):
    return vectorize([encode_text(text, vocab)])


def process(text):
    trans = str.maketrans('', '', string.punctuation)
    text = text.translate(trans).lower()

    words = []

    for word in word_tokenize(text):
        words.append(word)

    return words


def encode_text(text, vocab=None):
    data = []

    if vocab is None:
        with open(VOCAB_PATH, 'r', encoding='utf-8') as file:
            vocab = json.load(file)

    for word in process(text):
        if word in vocab:
            data.append(vocab[word])

    return data
