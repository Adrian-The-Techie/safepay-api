from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from decouple import config

# Create your views here.

@api_view(['POST'])
def index(request):

    requests.post(config('USSD_TEST_ENDPOINT'), json=request.data)

    return JsonResponse({"status": 1, "message": "USSD response"})