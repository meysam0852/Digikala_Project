from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def store_list(request):
    return HttpResponse("Stores")