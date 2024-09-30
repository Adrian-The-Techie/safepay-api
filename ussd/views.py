
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from decouple import config
import json

from user.models import User

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
    # response=""

    # print(params)

    # if params['menu_string'] == "":
    #     user = User.objects.filter(phone_number=params['msisdn'])

    #     if(len(user) > 0):
    #         # start 
    #         response ="CON Welcome " + user[0].first_name + " " + user[0].last_name + ", what would you like to do?\n1. Send money\n2. Request money\n3. Get my account balance"
    #     else:
    #         response = "END No such user found"
    
    # else:
    #     response = "END " + params['menu_string']

    response = requests.post(config('USSD_TEST_ENDPOINT'), params=params)

    print(response.json())

    return HttpResponse(response, content_type="text/plain")