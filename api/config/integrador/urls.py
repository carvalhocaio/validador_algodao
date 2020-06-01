from django.urls import path
from .views import integrador


urlpatterns = [
    path('', integrador, name='integrador')
]
