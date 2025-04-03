from .tanda import nameLookup

def sendMoneyFees(amount):

    # return 0
    if amount >=10 and amount <=999:
        return 50
    elif amount >=1000 and amount <=1499:
        return 60
    elif amount >=1500 and amount <=9999:
        return 70
    elif amount>=10000 and amount <=70000:
        return 120
    else:
        return 20
    
def payBillBuyGoodsFee(amount, shortcode, channel, type):
    # get shortcode 

    data={
        "shortcode":shortcode,
        "channel":channel,
        "type":type
    }

    res = nameLookup(data=data)

    print(res)

    # return 0
    if amount >=10 and amount <=999:
         res['fee'] =45
    elif amount >=1000 and amount <=1499:
        res['fee']= 55
    elif amount >=1500 and amount <=9999:
        res['fee']= 65
    elif amount>=10000 and amount <=70000:
        res['fee']= 120
    else:
        res['fee']=20
    
    return res