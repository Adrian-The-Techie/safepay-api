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

def _getAction(action):
    if action == "deposit":
        return "CustomerPayment"
    elif action == "sendMoney":
        return "CDeposit"
    elif action == "buyAirtime":
        return "TopupFlexi"
    elif action == "buyGoods":
        return "BuyGoods"
    elif action == "payBill":
        return "BillPay"
    else:
        return "INVALID"


def _getRequestParameters(action, data):
    requestParameters=[
            {
                "id": "amount",
                "value": data['amount'],
                "label": "Amount"
            },
            
        ]

    if action == "CustomerPayment" or action == "CDeposit" or action == "TopupFlexi":
        requestParameters.append({
                "id": "accountNumber",
                "value":  data['recipient'] if action == "CDeposit" or action == "TopupFlexi" else data['accountNumber'],
                "label": "AccountNumber"
        })
    if action == "BuyGoods":
        requestParameters.append(
            
            {
                "id": "merchantNumber" ,
                "value": data['recipient'],
                "label": "merchantNumber"
            },
        )
    
    if action == "BillPay":
        requestParameters.append(
            {
                "id": "businessNumber" ,
                "value": data['recipient'],
                "label": "BusinessNumber"
            },
        )
        requestParameters.append({
                "id": "accountNumber" ,
                "value": data['receiverAccount'],
                "label": "accountNumber"
            },)

    
    return requestParameters


def transact(data, channel="mobile"):
    print(data)
    commandID= _getAction(action=data['action'])
    requestParameters= _getRequestParameters(commandID, data)
    payload = {
        "commandId": commandID,
        "serviceProviderId": "MPESA" if data['action'] == "deposit" or data['action'] == "buyGoods" or data['action'] == "payBill" else data['serviceProvider'],
        "requestParameters": requestParameters,
        "referenceParameters":[
            {
                "id":"resultUrl",
                "value":f"{config('LIVE_ENDPOINT')}/api/v1/payments/result?action={data['action']}&channel={channel}",
            }
        ],
        "reference":data["reference"]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {generateToken()['access_token']}"
    }

    response = requests.post(REQUEST_URL, json=payload, headers=headers)

    return response.json()
