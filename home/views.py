from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.


def home_test(request: HttpRequest):
    return HttpResponse("This would be the home page")
