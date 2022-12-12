from flask import Flask, request, render_template
# from flask_restx import Resource, Api
# from controller.ClassifierController import ClassifierController
from classifierModel.data_preprocessing import PreProcessing
from classifierModel.data_loader import DataSet
from tensorflow.keras.models import load_model
import numpy as np
from DonggukJaws.service.slackService import sendToSlack, processTag
import operator
from konlpy.tag import Okt, Kkma


class ModelService :
    # Todo Model Singleton

    def __init__(self):
        self.posNegModel = self.loadPosNegModel()
        self.classClassifierModel = self.loadClassClassifier()

    def sentencePosOrNegService(self, input_sentence):
        global preprocessor
        model = self.loadPosNegModel()
        preprocessed_sentence = preprocessor.preprocess_sentence(input_sentence)
        return self.predictPosOrNeg(model, preprocessed_sentence)

    def loadPosNegModel(self):
        return load_model('./data/dl/best_model.h5')

    def evaluateTestDataset(self, model, X_test, y_test):
        print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]))

    def predictPosOrNeg(self, sentence):
        score = float(self.posNegModel.predict(sentence))  # 예측
        if (score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
            return True
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
            return False


    def loadClassClassifier(self):
        return load_model('./data/dl/classClassifier.h5')

    def predictClass(self, sentence):
        softmax = self.classClassifierModel.predict(sentence)
        output = np.argmax(softmax)
        return softmax, output

dataLoader = DataSet('data/ratings_train.txt', 'data/ratings_test.txt', 'data/pos_neg_genie_review_dataset.txt')
preprocessor = PreProcessing(dataLoader.train, dataLoader.test, True)
model_service = ModelService()
okt = Okt()

app = Flask(__name__)

# api = Api(app)
#
# api.add_namespace(ClassifierController, '/nlpmodel')

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/predictPosNeg', methods=['POST'])
def predict():
    input_sentence = request.form['input']
    print("Predict input : ", input_sentence)
    model_service = ModelService()
    return model_service.sentencePosOrNegService(input_sentence)

@app.route('/predictReview', methods=['POST'])
def predictReview():
    global model_service
    global okt
    input_paragraph = request.form['review']
    print("Input Paragraph : ", input_paragraph)
    posNegResult = list()
    classClassifierResult = list()
    classOutputs = list()

    average_softmax = [0 for i in range(6)]
    maxSoftmaxByClass = [ dict() for i in range(6)]

    negative = 0
    print(average_softmax)

    ## 1. 문단을 문장으로
    sentences = preprocessor.paragraphToSentences(input_paragraph)

    ## 2. for sentence in paragraph
    for idx, sentence in enumerate(sentences) :
        print(f'{idx} sentence : {sentence}')
        ## 3. text preprocessing
        posNegInputSentnece = preprocessor.preprocessingSentence(sentence)
        ## 4. pos / neg classification
        if not model_service.predictPosOrNeg(posNegInputSentnece) :
            ## 5. if neg -> Classification
            classInputSentence = preprocessor.preprocessingSentence(sentence,"Class")
            softmax, output = model_service.predictClass(classInputSentence)
            ## 6. [output -> pos / neg , softmax output value, model inference Class Info]
            print(softmax, output)
            if output != 0:
                negative += 1
                average_softmax = [x + y for x, y in zip(softmax[0], average_softmax)]
                maxSoftmaxByClass[output][idx] = softmax[0][output]
            posNegResult.append('부정')
            classClassifierResult.append(getClassName(output))
            classOutputs.append(output)
        else:
            posNegResult.append('긍정')
            classClassifierResult.append('긍정')
            classOutputs.append(-1)

    ## Logic
    average_softmax = [x / negative for x in average_softmax]
    print(average_softmax)
    print(np.argmax(average_softmax[1:]) + 1)

    final_class = np.argmax(average_softmax[1:]) + 1
    threshold = 0.35
    for classNum in range(1, 6):
        if average_softmax[classNum] >= threshold:
        # slack api
            techTags = list()
            techType = ['X', '앱 클라이언트 기능 문제', '서버 기능 문제', '사용자 개선 요구 사항', '음원 관련 이슈', '네트워크 이슈']

        # 기능 태그
        # 해당 클래스 문장 -> 탐색 키워드 있으면 출력
            classSentences = list()
            for idx, result in enumerate(classOutputs):
                if result == classNum:
                    classSentences.append(sentences[idx])

            print(" ".join(classSentences))
            techTags = processTag(classNum, " ".join(classSentences), okt)
            print(techTags)
            techTagsString = "`#" + "` `#".join(techTags)
            print(techTagsString)
        # 주요 이슈 -> 해당 클래스 중 가장 확률이 높은 문장
            importantIssueSentence = sentences[max(maxSoftmaxByClass[classNum].items(), key=operator.itemgetter(1))[0]]
            print(importantIssueSentence)
            sendToSlack(classNum, input_paragraph, techType[classNum], importantIssueSentence, techTagsString)



    return render_template('result.html', content=input_paragraph, splitArr=sentences, sentimentArr=posNegResult,
                           classifiedArr=classClassifierResult)

def getClassName(input_class) :
    classifiedArr = ['단순 부정', '앱 개발팀', '서비스 개발팀', '서비스 기획팀',
                     '콘텐츠 운영팀', 'IT 기획팀']
    return classifiedArr[input_class]

    '''
    1. 문장 나눈 결과
    2. 긍정 / 부정
    3. 문장별 최종 클래스 결과
    '''



if __name__ == '__main__':
    app.run(host="localhost", port=8080)