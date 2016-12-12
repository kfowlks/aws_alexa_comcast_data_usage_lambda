from __future__ import print_function
# -*- coding: utf-8 -*-
"""Comcast Internet Usage Alexa Skill
Author: Kevin Fowlks
Date:   12/05/2016

The comcast python code was stolen from https://github.com/lachesis/comcast

"""
from ask import alexa
#from dateutil.parser import parse
from datetime import datetime

import logging
import os
import re
import requests
import datetime
import json
import calendar
import time

class MyUsage(object):
    monthLongName = ""
    unitOfMeasure = ""
    homeUsage=0
    allowableUsage=1000

    # The class "constructor" - It's actually an initializer 
    def __init__(self, monthLongName, unitOfMeasure, homeUsage, allowableUsage):
        self.monthLongName = monthLongName
        self.unitOfMeasure = unitOfMeasure
        self.homeUsage = homeUsage
        self.allowableUsage = allowableUsage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.ERROR)

def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''
    

    metadata  = request.metadata

    if 'usageMonths' not in metadata:
        jsonStr = getUsage()

        if jsonStr == None:
            card = alexa.create_card(title="GetInternetUsage activated", subtitle=None,
                                    content="asked alexa to get internet usage")
            return alexa.create_response("Sorry unable to retrieve comcast account information", end_session=True, card_obj=card)

        jsonObj = json.loads(jsonStr)

        usageMonths = jsonObj['usageMonths']

        metadata = {'usageMonths' : usageMonths } # add your own metadata to the request using key value pairs

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask").with_card('What is my current internet usage')


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Hello Welcome to Internet Usage!")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler('GetInternetUsage')
def get_internet_usage_intent_handler(request):
    
    myUsageMonths = {}

    usageMonths = request.metadata['usageMonths']
    
    for usageMonth in usageMonths:
        monthName = calendar.month_name[int(usageMonth['startDate'][:2])]
        myUsageMonths[monthName] = MyUsage( monthName, usageMonth['unitOfMeasure'], usageMonth['homeUsage'], usageMonth['allowableUsage'])
    
    requestMonth = request.slots["Date"]

    if requestMonth == None:
        currentDT = datetime.datetime.now()  # If users request does not have a date lets default to the current date 
        requestUserMonthByName = currentDT.strftime("%B") # Get Month by name e.g.    
    else:    
        requestUserMonthByName = calendar.month_name[int(requestMonth[5] + requestMonth[6])]

    if requestUserMonthByName not in myUsageMonths:
        card = alexa.create_card(title="GetInternetUsage activated", subtitle=None,
                                 content="asked alexa to get internet usage using {}".format(requestMonth))
        return alexa.create_response("Sorry no usage data exist for the requested month {}".format(requestMonth), end_session=False, card_obj=card)
    else:
        return alexa.create_response("You have used %s%s out of %s%s for the month of %s!" % (myUsageMonths[requestUserMonthByName].homeUsage, 
                                                                                              myUsageMonths[requestUserMonthByName].unitOfMeasure, 
                                                                                              myUsageMonths[requestUserMonthByName].allowableUsage,
                                                                                              myUsageMonths[requestUserMonthByName].unitOfMeasure,
                                                                                              myUsageMonths[requestUserMonthByName].monthLongName ))
def getUsage():
    session = requests.Session()

    username = os.environ['COMCAST_USERNAME']
    password = os.environ['COMCAST_PASSWORD']

    logger.debug("Finding req_id for login...")
    res = session.get('https://login.comcast.net/login?r=comcast.net&s=oauth&continue=https%3A%2F%2Flogin.comcast.net%2Foauth%2Fauthorize%3Fclient_id%3Dmy-account-web%26redirect_uri%3Dhttps%253A%252F%252Fcustomer.xfinity.com%252Foauth%252Fcallback%26response_type%3Dcode%26state%3D%2523%252Fdevices%26response%3D1&client_id=my-account-web')

    if res.status_code != 200:
        return None

    m = re.search(r'<input type="hidden" name="reqId" value="(.*?)">', res.text)
    req_id = m.group(1)
    logger.debug("Found req_id = %r", req_id)

    data = {
        'user': username,
        'passwd': password, 
        'reqId': req_id,
        'deviceAuthn': 'false',
        's': 'oauth',
        'forceAuthn': '0',
        'r': 'comcast.net',
        'ipAddrAuthn': 'false',
        'continue': 'https://login.comcast.net/oauth/authorize?client_id=my-account-web&redirect_uri=https%3A%2F%2Fcustomer.xfinity.com%2Foauth%2Fcallback&response_type=code&state=%23%2Fdevices&response=1',
        'passive': 'false',
        'client_id': 'my-account-web',
        'lang': 'en',
    }

    logger.debug("Posting to login...")
    res = session.post('https://login.comcast.net/login', data=data)
    
    if res.status_code != 200:
        return None

    logger.debug("Fetching internet usage AJAX...")
    res = session.get('https://customer.xfinity.com/apis/services/internet/usage')
    
    if res.status_code != 200:
        return None

    return res.text