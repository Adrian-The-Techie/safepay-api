import requests
from decouple import config


REQUEST_URL=f"{config('TANDA_LIVE_ENDPOINT')}/io/v2/organizations/{config('ORG_ID')}/requests"
def generateToken():
    url = f"{config('TANDA_LIVE_ENDPOINT')}/accounts/v1/oauth/token"

    payload = {
        "grant_type": "client_credentials", 
        "client_id":config('CLIENT_ID'), 
        "client_secret":config('CLIENT_SECRET') 
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    return response.json()


def deposit(data):
    payload = {
        "commandId": "CustomerPayment",
        "serviceProviderId": data['serviceProvider'],
        "requestParameters":[
            {
                "id":"amount",
                "value":data['amount'],
            },
            {
                "id":"accountNumber",
                "value":data['accountNumber'],
            },
        ],
        "referenceParameters":[
            {
                "id":"resultUrl",
                "value":f"{config('LIVE_ENDPOINT')}/",
            }
        ],
        "reference":data["referenceNo"]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {generateToken()['access_token']}"
    }

    response = requests.post(REQUEST_URL, json=payload, headers=headers)
    print(response.text)

    return response.json()

def disburse(data):

    payload = {
        "commandId": "CDeposit",
        "serviceProviderId": data['serviceProvider'],
        "amount":data['amount'],
        "accountNumber":data['recipient'],
        "resultUrl":f"{config('LIVE_ENDPOINT')}/"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(REQUEST_URL, json=payload, headers=headers)
    print(response.text)

    return response.json()


def transactionFees():

    return 1