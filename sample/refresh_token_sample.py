﻿import json
import logging
import os
import sys
import adal

def turn_on_logging():
    logging.basicConfig(level=logging.DEBUG)
    #or, 
    #handler = logging.StreamHandler()
    #adal.set_logging_options({
    #    'level': 'DEBUG',
    #    'handler': handler 
    #})
    #handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))

# You can override the account information by using a JSON file. Either
# through a command line argument, 'python sample.js parameters.json', or
# specifying in an environment variable of ADAL_SAMPLE_PARAMETERS_FILE.
# {
#   "tenant" : "rrandallaad1.onmicrosoft.com",
#   "authorityHostUrl" : "https://login.microsoftonline.com",
#   "clientid" : "624ac9bd-4c1c-4687-aec8-b56a8991cfb3",
#   "username" : "user1",
#   "password" : "verySecurePassword"
# }

parameters_file = (sys.argv[1] if len(sys.argv) == 2 else 
                   os.environ.get('ADAL_SAMPLE_PARAMETERS_FILE'))

if parameters_file:
    with open(parameters_file, 'r') as f:
        parameters = f.read()
    sample_parameters = json.loads(parameters)
else:
    raise ValueError('Please provide parameter file with account information.')

authority_url = (sample_parameters['authorityHostUrl'] + '/' + 
                 sample_parameters['tenant'])
RESOURCE = '00000002-0000-0000-c000-000000000000'

#uncomment for verbose log
#turn_on_logging()

context = adal.AuthenticationContext(authority_url)

token = context.acquire_token_with_username_password(
    RESOURCE, 
    sample_parameters['username'],
    sample_parameters['password'],
    sample_parameters['clientid'])

print('Here is the token')
print(json.dumps(token, indent=2))

refresh_token = token['refreshToken']
token = context.acquire_token_with_refresh_token(
    refresh_token,
    sample_parameters['clientid'],
    RESOURCE)

print('Here is the token acquired from the refreshing token')
print(json.dumps(token, indent=2))
