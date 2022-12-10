import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from konlpy.tag import Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import kss
import pickle

class PreProcessing :
    def __init__(self, train_dataset, test_dataset, predefined = False) :
        self.okt = Okt()
        self.tokenizer = Tokenizer()
        self.stopWords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        self.max_len = 30
        self.train_dataset = train_dataset
        self.test_dataset = test_dataset
        self.y_train = np.array(train_dataset['label'])
        self.y_test = np.array(test_dataset['label'])
        self.X_train = train_dataset
        self.X_test = test_dataset
        print(len(self.train_dataset), len(self.test_dataset), type(self.train_dataset), type(self.test_dataset))
        if not predefined:
            self.makePreProcessor()
        else:
            with open('data/tokenizer/posNegTokenizer.pickle', 'rb') as handle:
                self.posNegTokenizer = pickle.load(handle)
            with open('data/tokenizer/ClassTokenizer.pickle', 'rb') as handle:
                self.classTokenizer = pickle.load(handle)

    def makePreProcessor(self):
        self.removeDuplicates()
        self.X_train = self.dataPreprocessor(self.train_dataset)
        self.X_test  = self.dataPreprocessor(self.test_dataset)
        print(len(self.X_train), len(self.X_test))
        self.makeWordTokenize(self.X_train, self.X_test, self.y_train, self.y_test)

    def dataPreprocessor(self, data_set):
        print(len(data_set), type(data_set))
        # data_set = self.removeNullData(data_set)
        # data_set = self.removeNotKoreanAndNotPolicy(data_set)
        # data_set = self.tokenizeKorean(data_set)
        return self.tokenizeKorean(self.removeNotKoreanAndNotPolicy(self.removeNullData(data_set)))


    def removeDuplicates(self):
        self.train_dataset.drop_duplicates(subset=['document'], inplace=True)
        self.test_dataset.drop_duplicates(subset=['document'], inplace=True)

    def removeNullData(self, data_set):
        print(len(data_set))
        data_set = data_set.dropna(how='any')
        return data_set

    def removeNotKoreanAndNotPolicy(self, data_set):
        data_set['document'] = data_set['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
        data_set['document'] = data_set['document'].str.replace('^ +', "")  # white space 데이터를 empty value로 변경
        data_set['document'].replace('', np.nan, inplace=True)
        data_set = data_set.dropna(how='any')
        return data_set

    def tokenizeKorean(self, data_set):
        preprocess_dataset = []
        for sentence in tqdm(data_set['document']):
            tokenized_sentence = self.okt.morphs(sentence, stem=True)  # 토큰화
            stopwords_removed_sentence = [word for word in tokenized_sentence if not word in self.stopWords]  # 불용어 제거
            preprocess_dataset.append(stopwords_removed_sentence)
        return preprocess_dataset

    def below_threshold_len(self, max_len, nested_list):
        count = 0
        for sentence in nested_list:
            if len(sentence) <= max_len:
                count = count + 1
        print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s' % (max_len, (count / len(nested_list)) * 100))

    def makeWordTokenize(self, X_train, X_test, y_train, y_test):
        print(X_train)
        print(X_test)
        print(y_train)
        print(y_test)
        self.tokenizer.fit_on_texts(X_train)
        print(self.tokenizer.word_index)
        threshold = 3
        total_cnt = len(self.tokenizer.word_index)  # 단어의 수
        rare_cnt = 0  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
        total_freq = 0  # 훈련 데이터의 전체 단어 빈도수 총 합
        rare_freq = 0  # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

        # 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
        for key, value in self.tokenizer.word_counts.items():
            total_freq = total_freq + value

            # 단어의 등장 빈도수가 threshold보다 작으면
            if value < threshold :
                rare_cnt = rare_cnt + 1
                rare_freq = rare_freq + value

        print('단어 집합(vocabulary)의 크기 :', total_cnt)
        print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s' % (threshold - 1, rare_cnt))
        print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt) * 100)
        print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq) * 100)
        # 전체 단어 개수 중 빈도수 2이하인 단어는 제거.
        # 0번 패딩 토큰을 고려하여 + 1
        vocab_size = total_cnt - rare_cnt + 1
        print('단어 집합의 크기 :', vocab_size)
        self.tokenizer = Tokenizer(vocab_size)
        self.tokenizer.fit_on_texts(X_train)
        self.X_train = self.tokenizer.texts_to_sequences(X_train)
        self.X_test = self.tokenizer.texts_to_sequences(X_test)

        drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]

        # 빈 샘플들을 제거
        self.X_train = np.delete(X_train, drop_train, axis=0)
        self.y_train = np.delete(y_train, drop_train, axis=0)
        print(len(self.X_train))
        print(len(self.y_train))
        if len(self.y_train) != len(self.X_train):
            print("Error : ", False)
            return

        self.below_threshold_len(self.X_train)

        self.X_train = pad_sequences(self.X_train, maxlen=self.max_len)
        self.X_test = pad_sequences(self.X_test, maxlen=self.max_len)

        return self.X_train, self.X_test, self.y_train, self.y_test

    def preprocess_sentence(self, input_sentence):
        input_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', input_sentence)
        new_sentence = self.okt.morphs(input_sentence, stem=True)  # 토큰화
        new_sentence = [word for word in new_sentence if not word in self.stopWords]  # 불용어 제거
        encoded = self.tokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=self.max_len)  # 패딩

        return pad_new

    def preprocessingSentence(self, input_sentence, type = "PosNeg"):
        input_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', input_sentence)
        new_sentence = self.okt.morphs(input_sentence, stem=True)  # 토큰화
        new_sentence = [word for word in new_sentence if not word in self.stopWords]  # 불용어 제거
        if type == "PosNeg":
            encoded = self.posNegTokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
        else:
            encoded = self.classTokenizer.texts_to_sequences([new_sentence])  # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=self.max_len)  # 패딩

        return pad_new


    def paragraphToSentences(self, input_paragraph):
        print("Input Raw Review : ", input_paragraph)
        sentences = kss.split_sentences(input_paragraph)
        for sentence in sentences:
            print(sentence)

        return sentences
