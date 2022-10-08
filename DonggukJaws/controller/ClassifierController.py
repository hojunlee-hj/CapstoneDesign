# from flask import Flask
# from flask_restx import RestError, Api, Namespace
# from service.modelService import ModelService
#
# ClassifierController = Namespace('ClassifierController')
#
# @ClassifierController.route('/predict/<string::input_sentence>')
# class ClassifierController :
#     def post(self, input_sentence):
#         return ModelService.predictPosOrNeg(input_sentence)
