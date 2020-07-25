from flask import Flask, request
from flask_restful import Resource, Api
from API.suggestion.suggestion import SuggestionAPI
from API.hotwords.hotwords import HotWordsAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(HotWordsAPI, '/api/sentiment/hotwords/<string:date>/')
api.add_resource(SuggestionAPI, '/api/sentiment/suggestion/<string:date>/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)