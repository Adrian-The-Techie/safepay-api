def sendMoneyFees(amount):

    return 0
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
    
def payBillBuyGoodsFee(amount):

    return 0
    if amount >=10 and amount <=999:
        return 45
    elif amount >=1000 and amount <=1499:
        return 55
    elif amount >=1500 and amount <=9999:
        return 65
    elif amount>=10000 and amount <=70000:
        return 120
    else:
        return 20