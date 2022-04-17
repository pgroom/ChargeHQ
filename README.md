NOT CURRENTLY WORKING
ChargeHQ is rejecting my siteId. The json looks correct so waiting Jay to check and advise.

An attempt at a Python script to take solar data from my local Enphase Envoy
and push it to the ChargeHQ API to allow me to charge my EV from excess solar.

Relies on Envoy being the older version 5 firmware. Version 7 will break the http auth and
require further work. Uses the Envoy production.json data.

Requires a config.py file in the same directory with the following format;
source = 'http://<ip of your local envoy>/production.json'
siteId = '<your siteId as provided by ChargeHQ>'
endPoint = 'https://<ChargeHQ API URL as provided by Jay>'

POST's the following json to ChargeHQ [NOT CURRENTLY WORKING];
{"SiteMeterPush": {"siteId": "not_telling", "siteMeters": {"production_kw": 0.0, "net_import_kw": 0.00, "consumption_kw": 0.00}}}

Full API not documented here as Jay may not want that made public



