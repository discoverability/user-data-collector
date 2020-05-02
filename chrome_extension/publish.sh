WS_CLIENT_ID=121069493888-b0jr0ucbp2fo2v12rjv2ps8t9hm58kdb.apps.googleusercontent.com
WS_CLIENT_SECRET=IWleRiHSXVay4ySvSHoQM6I8
APP_ID=$1
FILE_NAME=$2

xdg-open "https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&client_id=$WS_CLIENT_ID&redirect_uri=urn:ietf:wg:oauth:2.0:oob"

echo "Please authorise the app and paste the code provided here by google"
read WS_CODE

#WS_CODE=4/zAGZnRjNU2ge_gqA6y5YSJRJUahh73rqdCgnZ32SOMapvHS4IwbCT98

curl "https://accounts.google.com/o/oauth2/token" -d \
"client_id=$WS_CLIENT_ID&client_secret=$WS_CLIENT_SECRET&code=$WS_CODE&grant_type=authorization_code&redirect_uri=urn:ietf:wg:oauth:2.0:oob" -q > access_token.json

export ACCESS_TOKEN=$(jq " .access_token " ./access_token.json)




curl \
-H "Authorization: Bearer $ACCESS_TOKEN" \
-H "x-goog-api-version: 2" \
-X PUT \
-T $FILE_NAME \
-v \
https://www.googleapis.com/upload/chromewebstore/v1.1/items/$APP_ID

curl \
-H "Authorization: Bearer $ACCESS_TOKEN"  \
-H "x-goog-api-version: 2" \
-H "Content-Length: 0" \
-X POST \
-v \
https://www.googleapis.com/chromewebstore/v1.1/items/$APP_ID/publish
