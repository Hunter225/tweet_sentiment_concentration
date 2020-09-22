from rest_framework import serializers
from .models import SuggestionSchema
import json

class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    previous_concentration = serializers.SerializerMethodField()
    current_concentration = serializers.SerializerMethodField()
    hotwords = serializers.SerializerMethodField()
    class Meta:
        model = SuggestionSchema
        fields = ('suggestion_date', 'suggestion', 'previous_concentration', 'current_concentration', 'hotwords')

    def get_current_concentration(self, suggestion):
        return suggestion.concentration.concentration_coefficient
        
    def get_previous_concentration(self, suggestion):
        return suggestion.concentration.previous_concentration.concentration_coefficient

    def get_hotwords(self, suggestion):
        return json.loads(suggestion.concentration.word_frequency)