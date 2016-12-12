from __future__ import print_function
# -*- coding: utf-8 -*-
"""Comcast Internet Usage Alexa Skill
Author: Kevin Fowlks
Date:   12/05/2016

The comcast python code was stolen from https://github.com/lachesis/comcast


{
   "courtesyUsed":0,
   "courtesyRemaining":2,
   "courtesyAllowed":2,
   "inPaidOverage":false,
   "usageMonths":[
      {
         "policyName":"Xfinity Data Plan",
         "startDate":"06/01/2016",
         "endDate":"06/30/2016",
         "homeUsage":1759.0,
         "allowableUsage":250,
         "unitOfMeasure":"GB",
         "devices":[

         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":0.0,
         "additionalUnitsPerBlock":null,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"suspended"
      },
      {
         "policyName":"Xfinity Data Plan",
         "startDate":"07/01/2016",
         "endDate":"07/31/2016",
         "homeUsage":2037.0,
         "allowableUsage":250,
         "unitOfMeasure":"GB",
         "devices":[

         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":0.0,
         "additionalUnitsPerBlock":null,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"suspended"
      },
      {
         "policyName":"Xfinity Data Plan",
         "startDate":"08/01/2016",
         "endDate":"08/31/2016",
         "homeUsage":1464.0,
         "allowableUsage":250,
         "unitOfMeasure":"GB",
         "devices":[

         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":0.0,
         "additionalUnitsPerBlock":null,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"suspended"
      },
      {
         "policyName":"Xfinity Data Plan",
         "startDate":"09/01/2016",
         "endDate":"09/30/2016",
         "homeUsage":704.0,
         "allowableUsage":250,
         "unitOfMeasure":"GB",
         "devices":[

         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":0.0,
         "additionalUnitsPerBlock":null,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"suspended"
      },
      {
         "policyName":"Xfinity Data Plan",
         "startDate":"10/01/2016",
         "endDate":"10/31/2016",
         "homeUsage":768.0,
         "allowableUsage":250,
         "unitOfMeasure":"GB",
         "devices":[

         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":0.0,
         "additionalUnitsPerBlock":null,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"suspended"
      },
      {
         "policyName":"1 Terabyte Data Plan",
         "startDate":"11/01/2016",
         "endDate":"11/30/2016",
         "homeUsage":866.0,
         "allowableUsage":1024.0,
         "unitOfMeasure":"GB",
         "devices":[
            {
               "id":"78:96:84:FA:2F:F0",
               "usage":866.0
            }
         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":10.0,
         "additionalUnitsPerBlock":50.0,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"limited"
      },
      {
         "policyName":"1 Terabyte Data Plan",
         "startDate":"12/01/2016",
         "endDate":"12/31/2016",
         "homeUsage":268.0,
         "allowableUsage":1024.0,
         "unitOfMeasure":"GB",
         "devices":[
            {
               "id":"78:96:84:FA:2F:F0",
               "usage":268.0
            }
         ],
         "additionalBlocksUsed":0.0,
         "additionalCostPerBlock":10.0,
         "additionalUnitsPerBlock":50.0,
         "additionalIncluded":0.0,
         "additionalUsed":0.0,
         "additionalPercentUsed":0.0,
         "additionalRemaining":0.0,
         "billableOverage":0.0,
         "overageCharges":0.0,
         "overageUsed":0.0,
         "currentCreditAmount":0,
         "maxCreditAmount":0,
         "policy":"limited"
      }
   ]
}


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

    metadata = {'user_name' : 'SomeRandomDude'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message="Just ask")


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Hello Welcome to Comcast Internet Usage!")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")


@alexa.intent_handler('GetInternetUsage')
def get_internet_usage_intent_handler(request):


    jsonStr = getUsage()
    jsonObj = json.loads(jsonStr)
    usageMonths = jsonObj['usageMonths']

    myUsageMonths = {}
    
    requestUserMonthByName = ""
    requestMonth = request.slots["Date"]

    if requestMonth == None:
        currentDT = datetime.datetime.now()    
        requestUserMonthByName = currentDT.strftime("%B") # Get Month by name e.g.    
    else:    
        requestUserMonthByName = calendar.month_name[int(requestMonth[5] + requestMonth[6])]

    for usageMonth in usageMonths:
        monthName = calendar.month_name[int(usageMonth['startDate'][:2])]
        myUsageMonths[monthName] = MyUsage( monthName, usageMonth['unitOfMeasure'], usageMonth['homeUsage'], usageMonth['allowableUsage'])

    if requestUserMonthByName not in myUsageMonths:
        card = alexa.create_card(title="GetInternetUsage activated", subtitle=None,
                                 content="asked alexa to get internet usage using {}".format(requestMonth))
        return alexa.create_response("Sorry no usage data exist for the requested month  {}".format(requestMonth), end_session=False, card_obj=card)

    return alexa.create_response("You have used %s%s out of %s%s for the month of %s!" % (myUsageMonths[requestUserMonthByName].homeUsage, 
                                                                              myUsageMonths[requestUserMonthByName].unitOfMeasure, 
                                                                              myUsageMonths[requestUserMonthByName].allowableUsage,
                                                                              myUsageMonths[requestUserMonthByName].unitOfMeasure,
                                                                              myUsageMonths[requestUserMonthByName].monthLongName ))
  
    #for element in jsonObj['usageMonths']:
    #    print element.startDate
    #    print element.homeUsage
    #"startDate":"12/01/2016",
    #         "endDate":"12/31/2016",
    #         "homeUsage":268.0,
    #        "allowableUsage":1024.0,
    # 
    #     return alexa.create_response("Could not find an ingredient!")

def getUsage():
    session = requests.Session()

    username = os.environ['COMCAST_USERNAME']
    password = os.environ['COMCAST_PASSWORD']

    logger.debug("Finding req_id for login...")
    res = session.get('https://login.comcast.net/login?r=comcast.net&s=oauth&continue=https%3A%2F%2Flogin.comcast.net%2Foauth%2Fauthorize%3Fclient_id%3Dmy-account-web%26redirect_uri%3Dhttps%253A%252F%252Fcustomer.xfinity.com%252Foauth%252Fcallback%26response_type%3Dcode%26state%3D%2523%252Fdevices%26response%3D1&client_id=my-account-web')
    assert res.status_code == 200
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
    assert res.status_code == 200

    logger.debug("Fetching internet usage AJAX...")
    res = session.get('https://customer.xfinity.com/apis/services/internet/usage')
    assert res.status_code == 200

    return res.text



# jsonStr = getUsage()
# jsonObj = json.loads(jsonStr)
# usageMonths = jsonObj['usageMonths']

# myUsageMonths = {}

# requestMonth = '2016-09-12'
# print ('Hello')
# print (  requestMonth[5] + requestMonth[6] )

# requestUserMonthByName = ""

# if requestMonth == None:
#     currentDT = datetime.datetime.now()    
#     requestUserMonthByName = currentDT.strftime("%B") # Get Month by name e.g.    
# else:    
#     requestUserMonthByName = calendar.month_name[int(requestMonth[5] + requestMonth[6])]

# jsonStr = getUsage()
# jsonObj = json.loads(jsonStr)
# usageMonths   = jsonObj['usageMonths']

# print (len(usageMonths))

# for usageMonth in usageMonths:
#     monthName = calendar.month_name[int(usageMonth['startDate'][:2])]
#     myUsageMonths[monthName] = MyUsage( monthName, usageMonth['unitOfMeasure'], usageMonth['homeUsage'], usageMonth['allowableUsage'])

# print (requestUserMonthByName)
# print (myUsageMonths[requestUserMonthByName].homeUsage)
# print (myUsageMonths[requestUserMonthByName].unitOfMeasure)
# print (myUsageMonths[requestUserMonthByName].allowableUsage)

# print ("You have used %s %s out of %s %s for the month of %s!" % (myUsageMonths[requestUserMonthByName].homeUsage, 
#                                                                 myUsageMonths[requestUserMonthByName].unitOfMeasure, 
#                                                                 myUsageMonths[requestUserMonthByName].allowableUsage,
#                                                                 myUsageMonths[requestUserMonthByName].unitOfMeasure,
#                                                                 myUsageMonths[requestUserMonthByName].monthLongName ))