
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
import requests
from decouple import config
import json

from payments.helpers.fees import payBillBuyGoodsFee, sendMoneyFees
from shared import format_phone_number
from user.models import User
from ussd.tasks import _getAction, _getDestChannel, collect, _getAirtimeDestChannel

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
    response="CON system under maintenance"

    splitUssdString = params['ussd_string'].replace('*98', '').split('*')

    print(splitUssdString)

    if len(splitUssdString) == 1 and splitUssdString[0] == "":
        response = "CON Welcome to Safepay. What would you like to do?\n1. Send money\n2. Buy airtime\n3. Buy goods\n4. Pay bills"
    
    # SEND MONEY FLOW
    elif len(splitUssdString) >= 1 and len(splitUssdString) < 6 and splitUssdString[0] == "1":
        if len(splitUssdString) == 2:
            response = "CON Enter phone number to send money to:"

        elif len(splitUssdString) == 3:
            response = "CON Enter amount to send:"

        elif len(splitUssdString) == 4:
            # calculate fees
            fees = sendMoneyFees(int(splitUssdString[3]))
            response = "CON Please review transaction: \nRecipient: " + splitUssdString[2] + "Destination channel : " + _getDestChannel(splitUssdString[1]) + "\nAmount: " + splitUssdString[3] + "\nFees: " + str(fees) + "\nTotal: " + str(int(splitUssdString[3]) + fees) + "\n\n1. Confirm\n2. Cancel"

        elif len(splitUssdString) == 5:
            if splitUssdString[4] == "1":
                response = "END Your transaction is being processed. Thank you for using Safepay"

                transactionPayload = {
                    "source": params['msisdn'],
                    "recipient": format_phone_number(splitUssdString[2]),
                    "destinationChannel": _getDestChannel(splitUssdString[1]),
                    "amount": splitUssdString[3],
                    "fee": sendMoneyFees(int(splitUssdString[3])),
                    "total": int(splitUssdString[3]) + sendMoneyFees(int(splitUssdString[3])),
                    "action":_getAction(splitUssdString[0])
                }

                collect.delay(transactionPayload)
                
            elif splitUssdString[4] == "2":
                response = "END Transaction cancelled"
        else:
            response = "CON Choose mobile channel you want to send to:\n1. Airtel Money\n2. M-PESA\n3. T-Kash\n4. Equitel"

     # BUY AIRTIME FLOW
    elif len(splitUssdString) >= 1 and len(splitUssdString) < 6 and splitUssdString[0] == "2":
        if len(splitUssdString) == 2:
            response = "CON Enter phone number to buy airtime to:"

        elif len(splitUssdString) == 3:
            response = "CON Enter amount to buy:"

        elif len(splitUssdString) == 4:
            # calculate fees
            fees = sendMoneyFees(int(splitUssdString[3]))
            response = "CON Please review transaction: \nRecipient: " + splitUssdString[2] + "\nDestination channel : " + _getAirtimeDestChannel(splitUssdString[1]) + "\nAmount: " + splitUssdString[3] + "\nFees: " + str(fees) + "\nTotal: " + str(int(splitUssdString[3]) + fees) + "\n1. Confirm\n2. Cancel"

        elif len(splitUssdString) == 5:
            if splitUssdString[4] == "1":
                response = "END Your transaction is being processed. Thank you for using Safepay"

                transactionPayload = {
                    "source": params['msisdn'],
                    "recipient": format_phone_number(splitUssdString[2]),
                    "destinationChannel": _getAirtimeDestChannel(splitUssdString[1]),
                    "amount": splitUssdString[3],
                    "fee": 0,
                    "total": int(splitUssdString[3]),
                    "action":_getAction(splitUssdString[0])
                }

                collect.delay(transactionPayload)
                
            elif splitUssdString[4] == "2":
                response = "END Transaction cancelled"
        else:
            response = "CON Choose mobile channel you want to buy to:\n1. Airtel\n2. Safaricom\n3. Telkom"


    # BUY GOODS FLOW

    elif len(splitUssdString) >= 1 and len(splitUssdString) < 5 and splitUssdString[0] == "3":
        if len(splitUssdString) == 2:
            response = "CON Enter amount to pay:"

        elif len(splitUssdString) == 3:
            # calculate fees
            fees = payBillBuyGoodsFee(int(splitUssdString[2]))
            response = "CON Please review transaction: \nTill number: " + splitUssdString[1] + "\nAmount: " + splitUssdString[2] + "\nFees: " + str(fees) + "\nTotal: " + str(int(splitUssdString[2]) + fees) + "\n1. Confirm\n2. Cancel"

        elif len(splitUssdString) == 4:
            if splitUssdString[3] == "1":
                response = "END Your transaction is being processed. Thank you for using Safepay"

                transactionPayload = {
                    "source": params['msisdn'],
                    "recipient": splitUssdString[1],
                    "destinationChannel": "SAFARICOM",
                    "amount": splitUssdString[2],
                    "fee": payBillBuyGoodsFee(int(splitUssdString[2])),
                    "total": int(splitUssdString[2]) + payBillBuyGoodsFee(int(splitUssdString[2])),
                    "action":_getAction(splitUssdString[0])
                }

                collect.delay(transactionPayload)
                
            elif splitUssdString[4] == "2":
                response = "END Transaction cancelled"
        else:
            response = "CON Enter till number to pay to:"

    # PAY BILLS FLOW
    
    elif len(splitUssdString) >= 1 and len(splitUssdString) < 6 and splitUssdString[0] == "4":
        if len(splitUssdString) == 2:
            response = "CON Enter account number:"

        elif len(splitUssdString) == 3:
            response = "CON Enter amount to pay:"

        elif len(splitUssdString) == 4:
            # calculate fees
            fees = sendMoneyFees(int(splitUssdString[3]))
            response = "CON Please review transaction:\nPaybill number: " + splitUssdString[1] + "\nAccount number : " + splitUssdString[2] + "\nAmount: " + splitUssdString[3] + "\nFees: " + str(fees) + "\nTotal: " + str(int(splitUssdString[3]) + fees) + "\n1. Confirm\n2. Cancel"

        elif len(splitUssdString) == 5:
            if splitUssdString[4] == "1":
                response = "END Your transaction is being processed. Thank you for using Safepay"

                transactionPayload = {
                    "source": params['msisdn'],
                    "recipient": splitUssdString[1],
                    "receiverAccount": splitUssdString[2],
                    "destinationChannel": "SAFARICOM",
                    "amount": splitUssdString[3],
                    "fee": payBillBuyGoodsFee(int(splitUssdString[3])),
                    "total": int(splitUssdString[3]) + payBillBuyGoodsFee(int(splitUssdString[3])),
                    "action":_getAction(splitUssdString[0]) 
                }

                collect.delay(transactionPayload)
                
            elif splitUssdString[4] == "2":
                response = "END Transaction cancelled"
        else:
            response = "CON Enter paybill number to pay to:"

    
     
    # else:
    #     response = "END " + params['menu_string']

    # res = requests.post(config('USSD_TEST_ENDPOINT'), params=params)

    # formattedRes=res.json()
    # print(formattedRes)

    # DEV MODE
    # return JsonResponse({
    #     "message": response
    # })

    # PROD MODE

    return HttpResponse(response, content_type="text/plain")