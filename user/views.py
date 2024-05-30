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

# from shared import generateRefNo

# Create your views here.

class UserView(APIView):
    def post(self, request):
        data=request.POST
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
        # sendSms(userInstance.phone_number, f"Welcome to Safepay. You account has been created successfully")

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
            raise Exception("User not found")
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
            ]
            if(user.secondary_phone != ""):
                phones.append(
                {
                    "id": user.secondary_phone,
                    "label": f"Secondary phone: {user.secondary_phone}",
                
                })


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
            {"status":0,"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
        )
