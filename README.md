# An Amazon Alexa skill for getting your comcast internet usage using Python for AWS Lambda 

### Installation
pip install requests -t <path to this project>

Note: This code uses ask-alexa-pykit release python_lambda_0.5_release 

git checkout python_lambda_0.5_release 

You'll need to contruct a zip file that contains all code and external libraries.

```bash
zip -r ask-alexa_comcast_data_usage_lambda.zip *
```

In the AWS Lambda console you need to do the below

Create a blank AWS Lambda function, be sure to select Alexa as the trigger

upload zip file i.e. ask-alexa_comcast_data_usage_lambda.zip

You'll need to set the below Environment variables in your AWS Lambda console

    COMCAST_USERNAME
    COMCAST_PASSWORD

You'll need to configure the AWS Alexa skill console and follow the steps to create a skill. You will find the 
intent scheme and the utterance text under ![Alt text](/test-data "Test Data")

###Testing

In the AWS Lambda console you'll need to select the new function and configure the below test request.

Actions->Configure test event

```json
{
  "session": {
    "sessionId": "SessionId.9da74599-e9d0-4d7e-ad2f-fc3369e79614",
    "application": {
      "applicationId": "amzn1.ask.skill.[unique id]"
    },
    "attributes": {},
    "user": {
      "userId": "amzn1.ask.account.[unique id]"
    },
    "new": true
  },
  "request": {
    "type": "IntentRequest",
    "requestId": "EdwRequestId.[unique id]",
    "locale": "en-US",
    "timestamp": "2016-12-12T01:09:50Z",
    "intent": {
      "name": "GetInternetUsage",
      "slots": {
        "Date": {
          "name": "Date",
          "value": "2016-12-12"
        }
      }
    }
  },
  "version": "1.0"
}
```

If everything worked, you'll see a response like the below.

```json
{
  "version": "1.0",
  "response": {
    "outputSpeech": {
      "text": "You have used 325.0GB out of 1024.0GB for the month of December!",
      "type": "PlainText"
    },
    "shouldEndSession": false
  },
  "sessionAttributes": {}
}
```

###Requires

* Python 2.7+

### Version
0.0.1