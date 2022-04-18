Python script to take solar data from my local Enphase Envoy and push it to the ChargeHQ API.  
Created to to allow me to charge my EV from excess solar.  

Works with version 5 Envoy firmware.   
Version 7 will break the http auth and require further work.   
Uses the Envoy production.json data.  

Requires a config.py file in the same directory with the following format;  
source = `'http://<ip of your local envoy>/production.json'`  
siteId = `'your siteId as provided by ChargeH>'`  
endPoint = `'https://<ChargeHQ API URL as provided by Jay>'`  

POST's the following json to ChargeHQ;  
{"SiteMeterPush": {"siteId": "not_telling", "siteMeters": {"production_kw": 0.0, "net_import_kw": 0.00, "consumption_kw": 0.00}}}  

Full API not documented here as Jay may not want that made public  



