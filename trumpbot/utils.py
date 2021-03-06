import string
import numpy as np
from nltk.tokenize import word_tokenize
import json
import hashlib
import base64


VOCAB_PATH = './trumpbot/vocab.json'


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


def hash_password(password):
    _hash = hashlib.md5(password.encode('utf-8'))
    return _hash.hexdigest()


def parse_basic_auth_header(header):
    auth_type, auth_string = header.split()

    s = base64.urlsafe_b64decode(auth_string)
    s = str(s, 'utf-8').strip()

    return s.split(":")