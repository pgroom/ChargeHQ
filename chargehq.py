#!/usr/bin/env python3

import urllib.request,json,requests
from config import *
from socket import timeout
from urllib.error import HTTPError, URLError

error = 'None'

# Grab local Envoy production json

try:
    with urllib.request.urlopen(source, timeout=5) as url:
        data = json.loads(url.read().decode())
except (HTTPError, URLError):
    error = 'http_error'
    print (error)
except socket.timeout:
    error = 'Timeout'
    print (error)
else:

# Massage Envoy json into ChargeHQ compatible json

    #print(json.dumps(data, indent = 4, sort_keys=True))

    consumption = round(data['consumption'][0]['wNow'] / 1000,2)
    production = round(data['production'][0]['wNow'] / 1000,2)
    grid = round(production - consumption,2)

    print ('Production: ' , production)
    print ('Consumption: ' , consumption)

    if grid <0:
        grid = abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy
    else:
        grid = -abs(grid) # Invert grid value from Envoy value to keep ChargeHQ happy

    print ('Grid: ' , grid)

# create new json

    jsondata = {}
    jsondata['SiteMeterPush'] = {}
    jsondata['SiteMeterPush']['siteId'] = siteId
    jsondata['SiteMeterPush']['siteMeters'] = {}
    jsondata['SiteMeterPush']['siteMeters']['production_kw'] = production
    jsondata['SiteMeterPush']['siteMeters']['net_import_kw'] = grid
    jsondata['SiteMeterPush']['siteMeters']['consumption_kw'] = consumption 
    json_dump = json.dumps(jsondata)
    
    print(json_dump)

# POST json to ChargeHQ

    header = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(endPoint, data=json_dump, headers=header)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
