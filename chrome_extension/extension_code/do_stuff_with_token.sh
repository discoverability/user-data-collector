WS_CLIENT_ID=121069493888-b0jr0ucbp2fo2v12rjv2ps8t9hm58kdb.apps.googleusercontent.com
WS_CLIENT_SECRET=IWleRiHSXVay4ySvSHoQM6I8



xdg-open "https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&client_id=$WS_CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob"


read WS_CODE

#WS_CODE=4/zAGZnRjNU2ge_gqA6y5YSJRJUahh73rqdCgnZ32SOMapvHS4IwbCT98

curl "https://accounts.google.com/o/oauth2/token" -d \
"client_id=$WS_CLIENT_ID&client_secret=$WS_CLIENT_SECRET&code=$WS_CODE&grant_type=authorization_code&redirect_uri=urn:ietf:wg:oauth:2.0:oob" -q > access_token.json

ACCESS_TOKEN=$(jq " .access_token " ./access_token.json)
