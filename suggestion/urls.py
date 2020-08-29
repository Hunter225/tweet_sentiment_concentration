from django.conf.urls import url
from rest_framework import routers
from .views import SuggestionViewSet

urlpatterns = [url(r'^api/sentiment/suggestion/(?P<suggestion_date>[^\s]+)/$', SuggestionViewSet.as_view(), name='suggestion')]