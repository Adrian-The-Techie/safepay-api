import requests
from decouple import config


def sendSms(phone_number, message):
    smsEndpoint = config("SMS_ENDPOINT")
    headers = {
        "Content-Type": "application/json",
    }
    print(message)

    data = {
        "SenderId": config("SMS_SENDER_ID"),
        "Message": message,
        "MobileNumbers": phone_number,
        "ApiKey": config("SMS_API_KEY"),
        "ClientId": config("SMS_CLIENT_ID"),
    }

    response = requests.get(smsEndpoint, params=data, headers=headers)
    
    print(response.url)

    return response