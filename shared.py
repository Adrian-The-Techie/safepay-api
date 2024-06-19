import random
from datetime import datetime

def generateRefNo():
    number = random.randrange(1, 999)
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = 8
    all = upper + str(number)
    randomString = "".join(random.sample(all, length))

    return randomString

def format_phone_number(phone_number):
    """
    Format phone number into the format 2547XXXXXXXX

    Arguments:
            phone_number (str) -- The phone number to format
    """

    if len(phone_number) < 9:
        raise Exception("Phone number too short")
    else:
        return "254" + phone_number[-9:]
    
