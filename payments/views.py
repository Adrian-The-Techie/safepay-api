from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Q, Sum

import ast

from payments.serializers import PayoutsSerializer
from .tasks import collect, payout
from .models import Payout

# Create your views here.

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def send(request):
    collect.delay(request.data, request.user.id)
    return JsonResponse( {
        "status":1,
        "message":"Transaction initiated"
    })
    

@api_view(['POST'])
def result(request):
    action = request.query_params['action']
    res=request.data

    payout.delay(action, res)
    return JsonResponse(
        {
            "status":1,
            "data":{
                "message":"Callback initiated"
            }
        }
    )
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getTransactions(request):
    payins=Payout.objects.filter(date_initiated__range=(request.GET['from'], request.GET['to']), user=request.user)
    serializedPayouts=PayoutsSerializer(payins, many=True)

    return JsonResponse({"status":1, "data":serializedPayouts.data})