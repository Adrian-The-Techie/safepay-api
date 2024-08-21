import requests
from decouple import config
import uuid
import json


def sendSms(messages):
    print(messages)
    smsEndpoint = config("SMS_ENDPOINT")
    headers = {
        "Content-Type": "application/json",
        "api-key": config("SMS_API_KEY")
    }

    data = {
            "profile_code": config('SMS_PROFILE_ID'),
            "messages": messages,
            "dlr_callback_url": "https://5aab-2c0f-2a80-10ee-3010-6dab-1016-7d3c-7b3a.ngrok-free.app"
        }
    

    response = requests.post(smsEndpoint, json=data, headers=headers)

    print(response.json())

    return response