from flask import Flask, request, render_template
# from flask_restx import Resource, Api
# from controller.ClassifierController import ClassifierController
from classifierModel.data_preprocessing import PreProcessing
from classifierModel.data_loader import DataSet
from tensorflow.keras.models import load_model
import numpy as np


dataLoader = DataSet('data/ratings_train.txt', 'data/ratings_test.txt', 'data/pos_neg_genie_review_dataset.txt')
preprocessor = PreProcessing(dataLoader.train, dataLoader.test, True)

app = Flask(__name__)

# api = Api(app)
#
# api.add_namespace(ClassifierController, '/nlpmodel')

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
    input_paragraph = request.form['review']
    print("Input Paragraph : ", input_paragraph)
    posNegResult = list()
    classClassifierResult = list()

    model_service = ModelService()
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
            posNegResult.append('부정')
            classClassifierResult.append(getClassName(output))
        else:
            posNegResult.append('긍정')
            classClassifierResult.append('긍정')

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