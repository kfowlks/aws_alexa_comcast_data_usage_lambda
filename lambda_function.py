# -*- coding: utf-8 -*-
"""Comcast Internet Usage Alexa Skill
Author: Kevin Fowlks
Date:   12/05/2016
"""

from ask import alexa

import datetime


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
    
    currentDT = datetime.datetime.now()
    
    requestMonth = currentDT.strftime("%B") # Get Month by name e.g.

    #requestMonth = request.slots["XYZ"]
    requestMonth = ""
    for s in request.slots:
        requestMonth = requestMonth + s

    # # Get variables like userId, slots, intent name etc from the 'Request' object

    usageAmt   = 1
    usageUnits = "Gigs"
    requestMonth = "April"
    
    #if requestMonth == None:
        

    # 
    #     return alexa.create_response("Could not find an ingredient!")
    # card = alexa.create_card(title="GetRecipeIntent activated", subtitle=None,
    #                          content="asked alexa to find a recipe using {}".format(ingredient))    
    # return alexa.create_response("Finding a recipe with the ingredient {}".format(ingredient),
    #                              end_session=False, card_obj=card)

    return alexa.create_response("You have used %s %s for the month of %s!" % (usageAmt, usageUnits, requestMonth ))
