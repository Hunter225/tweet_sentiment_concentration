from flask_restful import Resource
from flask import jsonify
from models.suggestion.suggestion import Suggestion as SuggestionModel

class SuggestionAPI(Resource):
    def get(self, date):
        print(date)
        suggestion = SuggestionModel.get(id = date).to_dict()
        suggestion['date'] = suggestion['date'].strftime("%Y-%m-%d")
        return jsonify(suggestion)