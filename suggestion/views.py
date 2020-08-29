from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SuggestionSerializer
from .models import SuggestionSchema
from datetime import datetime

class SuggestionViewSet(APIView):

    def get(self, request, *args, **kwargs):
        suggestion_date = kwargs.get('suggestion_date')
        if not suggestion_date:
            return Response({'msg':'Please input suggestion_date field'})

        suggestion_date = datetime.strptime(suggestion_date, '%Y-%m-%d')
        suggestion = SuggestionSchema.objects.get(suggestion_date = suggestion_date)
        serialized = SuggestionSerializer(suggestion)

        return Response(serialized.data)