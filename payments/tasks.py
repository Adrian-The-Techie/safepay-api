from celery import shared_task
from payments.models import Payin, Payout
from shared import generateRefNo
import uuid
import ast
from payments.helpers.tanda import transact
from user.models import User
from notify.helpers.sms import sendSms
from datetime import datetime
import pytz

def _getPayoutStatus(action):
    if action == "sendMoney":
        return "MONEY"
    elif action == "buyAirtime":
        return "AIRTIME"
    elif action == "buyGoods":
        return "GOODS PAYMENT"
    elif action == "payBill":
        return "BILL PAYMENT"

def _getPayoutType(action):
    if action == "sendMoney":
        return "SEND MONEY"
    elif action == "buyAirtime":
        return "BUY AIRTIME"
    elif action == "buyGoods":
        return "BUY GOODS"
    elif action == "payBill":
        return "PAY BILL"


@shared_task()
def notifyBySMS(messages):
    sendSms(messages)

@shared_task()
def collect(data, userId):
    payinData={
        "reference":generateRefNo(),
        "serviceProvider": data['serviceProvider'],
        "accountNumber": data['accountNumber'],
        "amount":data['amountAfterFee'],
        "action":"deposit"
    }

    disburseData={
        "serviceProvider":payinData['serviceProvider'],
        "recipient":data['receiver'],
        "amount":data['amount'], 
        "action":data['action'],
        "fee":data['fee']
    }
    if "receiverAccount" in data:
        disburseData["receiverAccount"]=data['receiverAccount']
    depoRes=transact(payinData)

    payin = Payin.objects.create(
        user=User.objects.get(id=userId),
        reference_no=payinData['reference'],
        amount=payinData['amount'],
        source_account=payinData['accountNumber'],
        responsePayload=depoRes,
        url=uuid.uuid4(),
        type="TRANSFER",
        notes=data['notes'],
        meta=disburseData
    )

@shared_task()
def payout(action, res):
    naiTime = datetime.now(pytz.timezone('Africa/Nairobi'))
    formatted_time = naiTime.strftime('%d-%m-%Y at %H:%M:%S')
    senderPhone=""
    if action == "deposit":
        if res['status'] == "000000":
            # update payin
            payin = Payin.objects.filter(reference_no = res['reference'])
            payin.update(callbackPayload = res, status="DEPOSITED")
            

            # disburse
            disburseData=ast.literal_eval(payin.first().meta) # convert meta string to dictionary
            disburseData['reference']=generateRefNo()

            disburseRes=transact(disburseData)

            payout = Payout.objects.create(
                user=payin.first().user,
                reference_no= disburseData['reference'],
                payin_ref_no=payin.first().reference_no,
                amount=disburseData['amount'],
                destination_account=disburseData['recipient'],
                responsePayload=disburseRes,
                url=uuid.uuid4(),
                fee=int(disburseData['fee']),
                type=_getPayoutType(disburseData['action'])
            )

        if res['status'] == "500000":
            payin = Payin.objects.filter(reference_no = res['reference']).update(callbackPayload = res, status=res['message'])

        
        # update payout
    else:
        if res['status'] == "000000":
            transactionType=_getPayoutType(action)
            # update payout
            payout = Payout.objects.filter(reference_no = res['reference'])
            payout.update(callbackPayload = res, message=f"{_getPayoutStatus(action)} DISBURSED", status="SUCCESSFUL")
            
            # update user account spending balance types
            user=payout.first().user
            if transactionType == "BUY AIRTIME":
                user.money_on_airtime += payout.first().amount
            elif transactionType == "BUY GOODS":
                user.money_on_buy_goods += payout.first().amount
            elif transactionType == "PAY BILL":
                user.money_on_paybill += payout.first().amount
            elif transactionType == "SEND MONEY":
                user.money_sent += payout.first().amount

            user.total_money_spent += payout.first().amount

            user.save()

            # send message
            senderPhone=Payin.objects.get(reference_no = payout.first().payin_ref_no).source_account
            if action == "sendMoney":
                receiverMessage=f"{payout.first().reference_no} confirmed. You have received Ksh{payout.first().amount} from SAFEPAY on {formatted_time}\n\nMPESA reference number: {res['resultParameters'][0]['value']}"
                senderMessage=f"{payout.first().reference_no} confirmed. You have successfully sent Ksh{payout.first().amount} through SAFEPAY to {res['resultParameters'][1]['value']} on {formatted_time}\n\nMPESA reference number: {res['resultParameters'][0]['value']}"
                messages=[
                    {
                        "mobile_number":payout.first().destination_account,
                        "message":receiverMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    },
                    {
                        "mobile_number":senderPhone,
                        "message":senderMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    }
                ]
            elif action == "buyAirtime":
                receiverMessage=f"{payout.first().reference_no} confirmed. You have received Ksh{payout.first().amount} airtime from SAFEPAY on {formatted_time}\n\nThird party reference number: {res['receiptNumber']}"
                senderMessage=f"{payout.first().reference_no} confirmed. You have successfully bought airtime worth Ksh{payout.first().amount} through SAFEPAY for  {payout.first().destination_account} on {formatted_time}\n\nThird party reference number: {res['receiptNumber']}"
                messages=[
                    {
                        "mobile_number":payout.first().destination_account,
                        "message":receiverMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    },
                    {
                        "mobile_number":senderPhone,
                        "message":senderMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    }
                ]
            elif action == "buyGoods":
                # receiverMessage=f"{payout.first().reference_no} confirmed. You have received Ksh{payout.first().amount} airtime from SAFEPAY on {formatted_time}\n\Third party reference number: {res['receiptNumber']}"
                senderMessage=f"{payout.first().reference_no} confirmed. You have successfully paid Ksh{payout.first().amount} through SAFEPAY for {payout.first().destination_account if res['resultParameters'][1]['value'] == '' else res['resultParameters'][1]['value']} on {formatted_time}\n\nMPESA reference number: {res['resultParameters'][0]['value']}"
                messages=[
                    # {
                    #     "mobile_number":payout.first().destination_account,
                    #     "message":receiverMessage,
                    #     "message_type": "transactional",
                    #     "message_ref": f"{uuid.uuid4()}"
                    # },
                    {
                        "mobile_number":senderPhone,
                        "message":senderMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    }
                ]
            elif action == "payBill":
                # receiverMessage=f"{payout.first().reference_no} confirmed. You have received Ksh{payout.first().amount} airtime from SAFEPAY on {formatted_time}\n\Third party reference number: {res['receiptNumber']}"
                senderMessage=f"{payout.first().reference_no} confirmed. You have successfully paid Ksh{payout.first().amount} through SAFEPAY for {payout.first().destination_account if res['resultParameters'][1]['value'] == '' else res['resultParameters'][1]['value']} on {formatted_time}\n\nMPESA reference number: {res['resultParameters'][0]['value']}"
                messages=[
                    # {
                    #     "mobile_number":payout.first().destination_account,
                    #     "message":receiverMessage,
                    #     "message_type": "transactional",
                    #     "message_ref": f"{uuid.uuid4()}"
                    # },
                    {
                        "mobile_number":senderPhone,
                        "message":senderMessage,
                        "message_type": "transactional",
                        "message_ref": f"{uuid.uuid4()}"
                    }
                ]
            # send message
            notifyBySMS.delay(messages)


        else:
            payout = Payout.objects.filter(reference_no = res['reference']).update(callbackPayload = res, message=res['message'], status="FAILED")




