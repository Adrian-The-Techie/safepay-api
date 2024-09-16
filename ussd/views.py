
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from decouple import config
import json

# Create your views here.

@api_view(['POST', 'GET'])
def index(request):

    requests.post(config('USSD_TEST_ENDPOINT'), data=request.data)

    return HttpResponse("System under maintenance")