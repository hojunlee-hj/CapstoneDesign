from flask import Flask, request, render_template
# from flask_restx import Resource, Api
# from controller.ClassifierController import ClassifierController
from classifierModel.data_preprocessing import PreProcessing
from classifierModel.data_loader import DataSet
from tensorflow.keras.models import load_model


dataLoader = DataSet('data/ratings_train.txt', 'data/ratings_test.txt', 'data/pos_neg_genie_review_dataset.txt')
preprocessor = PreProcessing(dataLoader.train, dataLoader.test)

app = Flask(__name__)
# api = Api(app)
#
# api.add_namespace(ClassifierController, '/nlpmodel')

class ModelService :
    # Todo Model Singleton

    def sentencePosOrNegService(self, input_sentence):
        global preprocessor
        model = self.loadModel()
        preprocessed_sentence = preprocessor.preprocess_sentence(input_sentence)
        return self.predictPosOrNeg(model, preprocessed_sentence)

    def loadModel(self):
        return load_model('./data/dl/best_model.h5')

    def evaluateTestDataset(self, model, X_test, y_test):
        print("\n 테스트 정확도: %.4f" % (model.evaluate(X_test, y_test)[1]))

    def predictPosOrNeg(self, model, sentence):
        print("Predict Sentence : ", sentence)
        score = float(model.predict(sentence))  # 예측
        if (score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
            response = score * 100
            return str(response)
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
            response = -(1 - score) * 100
            return str(response)

@app.route('/')
def hello_world():
    return render_template('input.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_sentence = request.form['input']
    print("Predict input : ", input_sentence)
    model_service = ModelService()
    return model_service.sentencePosOrNegService(input_sentence)


if __name__ == '__main__':
    app.run()