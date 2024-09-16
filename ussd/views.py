
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from decouple import config
import json

# Create your views here.

@api_view(['POST', 'GET'])
def index(request):

    params = {
        "session_id": request.GET['session_id'],
        "service_code": request.GET['service_code'],
        "msisdn": request.GET['msisdn'],
        "menu_string": request.GET['menu_string'],
        "ussd_string": request.GET['ussd_string']
    }

    print(params)

    response = requests.get(config('USSD_TEST_ENDPOINT'), params=params)

    return HttpResponse("END System under maintenance", content_type="text/plain")