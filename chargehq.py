#!/usr/bin/env python3

import json
import requests
import configparser
import jwt
import time
import os
from socket import timeout
from urllib.error import HTTPError, URLError

requests.packages.urllib3.disable_warnings()
error = 'None'

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__),'config.ini'))

user = config['ENPHASE']['user']
password = config['ENPHASE']['password']

source = config['ENVOY']['source']
envoy_serial = config['ENVOY']['envoy_serial']

endPoint = config['CHARGEHQ']['endPoint']
apiKey = config['CHARGEHQ']['apiKey']

token = config['SESSION']['token']
token_epoch = config['SESSION']['token_epoch']
if token_epoch:
   token_epoch=int(token_epoch)

# Check for token and obtain if nessecary
if token == "":
   print('token missing')
   token_needed=True
if token_epoch == "":
   print('token epoch missing')
   token_needed=True
   token_epoch=1
if token_epoch > 0:
   time_diff = token_epoch - time.time()
   if time_diff < 2592000:
      print('token found but expires in less than 30 days')
      token_needed=True 
   else:
      print('token found and does not need to be renewed')
      token_needed=False

if token_needed:
   print('obtaining token')
   data = {'user[email]': user, 'user[password]': password}
   response = requests.post('https://enlighten.enphaseenergy.com/login/login.json', data=data)
   response_data = json.loads(response.text)
   data = {'session_id': response_data['session_id'], 'serial_num': envoy_serial, 'username': user}
   response = requests.post('https://entrez.enphaseenergy.com/tokens', json=data)
   token = response.text

   decode = jwt.decode(token, options={"verify_signature": False}, algorithms="ES256", audience=envoy_serial)

   exp_epoch = decode["exp"]
   
   config['SESSION']['token_epoch'] = str(exp_epoch)
   config['SESSION']['token'] = token
   with open('config.ini', 'w') as configfile:
    config.write(configfile)

# Nasty hackz to get Enphase token/cookie garbage working

headers = {
   "Authorization": "Bearer " + token
}

response = requests.get(f'https://envoy.local/auth/check_jwt', headers=headers, verify=False)

if "Valid token." in response.text:
       sessionId = response.cookies['sessionId']


# Crappy hackz over, now begins the original code
# Grab local Envoy production json

headers = {
    "cookie": f"sessionId={sessionId}",
    "Authorization": f"Bearer {token}"
}

try:
    payload = ""
    headers = {
        "cookie": f"sessionId={sessionId}",
        "Authorization": f"Bearer {token}"
    }

    response = requests.request("GET", source, data=payload, headers=headers, verify=False)
    data = response.json()


except (HTTPError, URLError):
    error = 'http_error'
    print (error)
except socket.timeout:
    error = 'Timeout'
    print (error)
else:

# Massage Envoy json into ChargeHQ compatible json

    consumption = round(data['consumption'][0]['wNow'] / 1000,2)
    production = round(data['production'][0]['wNow'] / 1000,2)
    grid = round(production - consumption,2)

    if grid <0:
        grid = abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy
    else:
        grid = -abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy

# create new json

    jsondata = {}
    jsondata['apiKey'] = apiKey
    jsondata['siteMeters'] = {}
    jsondata['siteMeters']['production_kw'] = production
    jsondata['siteMeters']['net_import_kw'] = grid
    jsondata['siteMeters']['consumption_kw'] = consumption 
    json_dump = json.dumps(jsondata)
    
# POST json to ChargeHQ

    header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(endPoint, data=json_dump, headers=header)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
