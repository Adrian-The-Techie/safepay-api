from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import F, Q, Sum

import ast

from payments.serializers import PayoutsSerializer
from ussd.tasks import ussdPayout
from .tasks import collect, payout
from .models import Payout, Payin
from datetime import  datetime
from payments.helpers.fees import sendMoneyFees, payBillBuyGoodsFee

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import pytz



# Create your views here.

def _getPayoutDesc(action):
    if action == "SEND MONEY":
        return "Sent"
    elif action == "BUY AIRTIME":
        return "Bought"
    elif action == "BUY GOODS" or action == "PAY BILL":
        return "Paid"
    else:
        return "Invalid"

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
    channel=request.query_params['channel']
    res=request.data
    naiTime = datetime.now(pytz.timezone('Africa/Nairobi'))
    formatted_time = naiTime.strftime('%d-%m-%Y at %H:%M:%S')
    print(action)
    print("----------------------------------")
    print(res)

    if(channel == "ussd"):
        ussdPayout.delay(action, res)
    else:
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
@api_view(['POST'])
def getFees(request):
    type = request.query_params['type']
    fee=20
    amount=int(request.data['amount'])
    if type == "sendMoney":
        fee = sendMoneyFees(amount)
        amountAfterFee = amount + fee
    elif type == "buyAirtime":
        fee = 0
    elif type == "payBill" or type == "buyGoods":
        fee = payBillBuyGoodsFee(amount, request.data['shortcode'], request.data['channel'], type=type)
        
        amountAfterFee = amount + fee['fee']
    return JsonResponse(
        {
            "status":1,
            "data":{
                "amount":amount,
                "fee":fee['fee'],
                "merchant":fee['name'] if 'name' in fee else None,
                "amountAfterFee":amountAfterFee,
            }
        }
    )
    

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getTransactions(request):
    payouts=Payout.objects.filter(date_initiated__range=(request.GET['from'], request.GET['to']), user=request.user).order_by("-timestamp")
    serializedPayouts=PayoutsSerializer(payouts, many=True)

    for payout in serializedPayouts.data:
        dateObject=datetime.strptime(payout['timestamp'],"%Y-%m-%dT%H:%M:%S.%f%z")
        payout['desc']=f"{_getPayoutDesc(payout['type'])} on {datetime.strftime(dateObject,'%d-%m-%Y at %I:%M:%S%p')}"

    return JsonResponse({"status":1, "data":serializedPayouts.data})

@api_view(['GET'])
def update(request):
    payouts=Payout.objects.all()
    for p in payouts:
        if p.type == "SEND MONEY":
            p.user.money_sent += p.amount
            p.user.save()
        elif p.type == "PAY BILL":
            p.user.money_on_paybill += p.amount
            p.user.save()
        elif p.type == "BUY GOODS":
            p.user.money_on_buy_goods += p.amount
            p.user.save()
        elif p.type == "BUY AIRTIME":
            p.user.money_on_airtime += p.amount
            p.user.save()

        else:
            continue
        p.user.total_money_spent = p.user.money_on_airtime +p.user.money_on_paybill + p.user.money_on_buy_goods + p.user.money_sent
        p.user.save()
    return JsonResponse({
        "status":1,
        "message":"Split"
    })