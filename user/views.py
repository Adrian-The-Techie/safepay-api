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
            secondary_phone=format_phone_number(data['secondaryPhone']),
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
        sendSms(userInstance.phone_number, f"Welcome to Safepay. You account has been created successfully")

        return JsonResponse({
            "status":1,
            "message":"Registration successful",
        })

        # except Exception as e:
        #     return Response({
        #         "status":0,
        #         "error":f"{e}",
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(["POST"])
def login(request):
    try:
        user = User.objects.get(email=request.data["phone"])
        if check_password(request.data["password"], user.password) == False:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        else:
            token = Token.objects.get_or_create(user=user)[0].key

            response = {
                "status": 1,
                "message": "Login successful",
                "data": {
                    "user": {
                        "name": user.first_name,
                    },
                    "token": token,
                },
            }

        return JsonResponse(response)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User not found"}, status=status.HTTP_401_UNAUTHORIZED
        )
