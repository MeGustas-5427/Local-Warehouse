from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def help(request):
    return HttpResponse('help')