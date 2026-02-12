from django.urls import path
from . import views

urlpatterns= [
    path('violao/', views.aulas_violao, name= 'aulas violão'),
    path('flauta/', views.aulas_flauta, name='aulas de flauta')
]