from django.http import JsonResponse
from django.shortcuts import render
from .helpers.tanda import disburse, deposit
from rest_framework.decorators import api_view
from shared import generateRefNo

# Create your views here.

@api_view(['POST'])
def disburse(request):
    try:
        data={
            "referenceNo":generateRefNo(),
            "serviceProvider": request.data['serviceProvider'],
            "accountNumber": request.data['accountNumber'],
            "amount":request.data['amount'],
        }
        depoRes=deposit(data)

        print(depoRes)

        return JsonResponse( {
            "status":1,
            "message":"Success"
        })

        
    except Exception as e:
        return JsonResponse( {
            "status":0,
            "message":f"Error {e}"
        })