
# ChargeHQ

Python script to take solar data from a local Enphase Envoy and push it to the ChargeHQ API.  
Created because ChargeHQ is unable to support Enphase nativley due to Enphase 3rd party access policy. 

ChargeHQ specific information available from https://chargehq.net/kb/push-api

Known to work with version 7 Envoy firmware that forces use of a token and session cookie\
If you have version 5 Envoy firmware then try chargehq_v5.py\
Script grabs initial token file from Enphase using the credentials you supply in the config.ini file\
Script will renew the token when it has less than 30 days before expiry\
At the time of writing Enphase set token expiry to be twelve months

Uses the Envoy production.json data.  

crontab to run every minute, 5AM to 10PM daily; ` */1 5-21 * * * <path>/chargehq.py` 

Requires a config.ini file in the same directory

\[ENPHASE]\
user = \<your Enphase website username>\
password = \<your Enphase website password>

\[ENVOY]\
envoy_serial = \<your Enphase Envoy serial number>\
source = http://envoy.local/production.json (or change to suit your local setup)

\[CHARGEHQ]\
endpoint = https://api.chargehq.net/api/public/push-solar-data \
apikey = \<your ChargeHQ api key>

\[SESSION]\
token =\<leave blank>\
token_epoch =\<leave blank>


POST's the following json to ChargeHQ;  
{"apiKey": "not_telling", "siteMeters": {"production_kw": 0.00, "net_import_kw": 0.00, "consumption_kw": 0.00}}

Negative net_import = exporting

Old version 5 config instructions (ignore if using the v7 script);

Requires a config.py file in the same directory with the following format;  
source = `'http://<ip of your local envoy>/production.json'`    
endPoint = `'https://api.chargehq.net/api/public/push-solar-data>'`  
apiKey = `'<your apiKey from https://app.chargehq.net/config/energy-monitor>'`
