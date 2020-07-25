from flask_restful import Resource
from flask import jsonify
from models.concentration.concentration import Concentration as ConcentrationModel

class HotWordsAPI(Resource):
    def get(self, date):
        concentration = ConcentrationModel.get(id = date).to_dict()
        hotwords = dict(date=concentration['date'], hotwords=concentration['word_frequency'])
        return jsonify(hotwords)