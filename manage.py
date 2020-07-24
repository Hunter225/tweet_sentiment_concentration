from flask import Flask, request
from flask_restful import Resource, Api
from API.suggestion.suggestion import SuggestionAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(SuggestionAPI, '/sentiment/api/suggestion/<string:date>/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)