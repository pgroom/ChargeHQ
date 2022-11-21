Python script to take solar data from a local Enphase Envoy and push it to the ChargeHQ API.  
Created because ChargeHQ is unable to support Enphase nativley.  

ChargeHQ specific information available from https://chargehq.net/kb/push-api

Known to work with version 5 Envoy firmware. 

Uses the Envoy production.json data.  

crontab to run 5AM to 9PM daily;
*/1 5-21 * * * <path>/chargehq.py

Requires a config.py file in the same directory with the following format;  
source = `'http://<ip of your local envoy>/production.json'`    
endPoint = `'https://api.chargehq.net/api/public/push-solar-data>'`  
apiKey = `'<your apiKey from https://app.chargehq.net/config/energy-monitor>'`

POST's the following json to ChargeHQ;  
{"apiKey": "not_telling", "siteMeters": {"production_kw": 0.00, "net_import_kw": 0.00, "consumption_kw": 0.00}}

Negative net_import = exporting
