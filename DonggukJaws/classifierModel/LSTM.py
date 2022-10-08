import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class LSTM :
    def __init__(self, vocab_size):
        self.embedding_dim = 128
        self.hidden_units = 256
        self.vocab_size = vocab_size
        self.earlyStopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)
        self.modelCheckPoint = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
        self.model = self.makeModel()

    def makeModel(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, self.embedding_dim))
        model.add(LSTM(self.hidden_units))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])

        return model