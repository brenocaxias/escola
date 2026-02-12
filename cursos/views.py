from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def aulas_violao(request):
    return HttpResponse('Olá, testando aula de violão')
def aulas_flauta(request):
    return HttpResponse('Olá, aulas de flauta')