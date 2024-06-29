from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework import status 
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.authtoken.models import Token
from notify.helpers.sms import sendSms
from shared import format_phone_number, generateRefNo
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
import math
from payments.tasks import notifyBySMS
import uuid

# from shared import generateRefNo

# Create your views here.

class UserView(APIView):
    def post(self, request):
        data=request.data
        files=request.FILES
        print(data)
        
        # try:
        userInstance= User(
            first_name=data['firstName'],
            last_name=data['lastName'],
            phone_number=data['primaryPhone'],
            secondary_phone=data['secondaryPhone'],
            idNumber=data['idNumber'],
            username=generateRefNo(),
            email=data['email'],
            password=make_password(request.data["password"])
        )
        if data.get('frontID'):
            userInstance.id_front = files['frontID']

        if data.get('backID'):
            userInstance.id_front = files['backID']
        if data.get('selfie'):
            userInstance.id_front = files['selfie']

        userInstance.save()
        # send sms
        messages=[
            {
                "mobile_number":userInstance.phone_number,
                "message":"Welcome to Safepay. You account has been created successfully",
                "message_type": "transactional",
                "message_ref": f"{uuid.uuid4()}"
            },
        ]
        notifyBySMS.delay(messages)

        phones=[
            {
                "id": userInstance.phone_number,
                "label": f"Primary phone: {userInstance.phone_number}",
            },
        ]
        if(userInstance.secondary_phone != ""):
            phones.append(
               {
                "id": userInstance.secondary_phone,
                "label": f"Secondary phone: {userInstance.secondary_phone}",
            
            })

        return JsonResponse({
            "status":1,
            "message":"Registration successful",
            "data":{
                "primaryPhone":userInstance.phone_number,
                "first_name":userInstance.first_name,
                "phones":phones
            }
        })
    @permission_classes([IsAuthenticated])
    def put(self, request):
        user=User.objects.get(id=request.user.id)
        user.first_name = request.data['firstName']
        user.last_name = request.data['lastName']
        user.phone_number = request.data['primaryPhone']

        user.save()

        return JsonResponse({
            "status":1,
            "message":"Details updated successfully",
            "data":{
                    "primaryPhone":user.phone_number,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "phones":[
                        {
                            "id": user.phone_number,
                            "label": f"Primary phone: {user.phone_number}",
                        },
                        {
                            "id": "other",
                            "label": "Other",
                        }
                    ],
                    "token": Token.objects.get_or_create(user=user)[0].key,
                }
        })

        # except Exception as e:
        #     return Response({
        #         "status":0,
        #         "error":f"{e}",
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(["POST"])
def login(request):
    try:
        user = User.objects.get(phone_number=request.data["phone"])
        if check_password(request.data["password"], user.password) == False:
            return Response(
                {"status":0,"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        else:
            token = Token.objects.get_or_create(user=user)[0].key
            phones=[
                {
                    "id": user.phone_number,
                    "label": f"Primary phone: {user.phone_number}",
                },
                {
                    "id": "other",
                    "label": "Other",
                }
            ]

            response = {
                "status": 1,
                "message": "Login successful",
                "data": {
                    "primaryPhone":user.phone_number,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "phones":phones,
                    "token": token,
                },
            }

            return JsonResponse(response)
    except User.DoesNotExist:
        return JsonResponse(
            {"status":0,"error": "User not found. Please create account to Pay Safely"}, status=status.HTTP_404_NOT_FOUND
        )

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def getHomeData(request):
    totalMoneySpent=request.user.total_money_spent
    moneyOnAirtime=0
    moneyOnPaybill=0
    moneyOnBuyGoods=0
    moneySent=0
    if totalMoneySpent > 0:
        moneyOnAirtime=math.floor(((request.user.money_on_airtime/totalMoneySpent)*100))
        moneyOnPaybill=math.floor((request.user.money_on_paybill/totalMoneySpent)*100)
        moneyOnBuyGoods=math.floor((request.user.money_on_buy_goods/totalMoneySpent)*100)
        moneySent=math.floor((request.user.money_sent/totalMoneySpent)*100)

    return JsonResponse({
        "status":1,
        "message":"Home data",
        "data":{
            "totalMoneySpent":totalMoneySpent,
            "moneyOnAirtime":moneyOnAirtime,
            "moneyOnPaybill":moneyOnPaybill,
            "moneyOnBuyGoods":moneyOnBuyGoods,
            "moneySent":moneySent
        }
        
    })
