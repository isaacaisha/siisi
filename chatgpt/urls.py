# chatgpt/urls.py

from django.urls import path
from .views import index, response


urlpatterns = [
    path('', index, name='index'),
    path('index/response', response, name='response'),
]
