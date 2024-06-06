from django.http import JsonResponse
from django.shortcuts import render

from payments.models import Payin
from .helpers.tanda import disburse, deposit
from rest_framework.decorators import api_view
from shared import generateRefNo
from django.db.models import F, Q, Sum

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
        return JsonResponse({
            "status":0,
            "message":f"Error {e}"
        })
    

@api_view(['POST'])
def result(request):

    print(request.data)

    return JsonResponse(
        {
            "status":1,
            "data":{
                "message":"Successfull"
            }
        }
    )
    

@api_view(['GET'])
def getTransactions(request):
    payins=Payin.objects.filter(Q())