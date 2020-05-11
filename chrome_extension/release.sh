set -x 
set -e 
export TARGET_FOLDER=$1
echo "@@@ $TARGET_FOLDER"
export APP_NAME=$2
echo "@@@@ $APP_NAME"
export APP_NAME_ESCAPED=$(echo "$2" | tr " " -)
export APP_VERSION="$3"
echo "@@@@@$APP_VERSION"
export TARGET_SERVER="$4"
export DEV_BUILD="$5"

DIR="$(dirname "$0")"

export TARGET_FILE=$TARGET_FOLDER/manifest.json
cp manifest.master $TARGET_FILE 

#change metadata in manifest
jq ".version = \"$APP_VERSION\"" $TARGET_FILE  |sponge $TARGET_FILE 
jq ".name= \"$APP_NAME\"" $TARGET_FILE  |sponge $TARGET_FILE 
jq 'del(.content_scripts)' $TARGET_FILE  |sponge $TARGET_FILE 
jq ".permissions += [\"$TARGET_SERVER/\"]" $TARGET_FILE  |sponge $TARGET_FILE 
jq '.content_scripts += [{ "matches": ["https://*.netflix.com/*"], "js": ["server.js","global.js","netflix_lib.js","netflix.js"]}]' $TARGET_FILE  |sponge $TARGET_FILE 
jq ".content_scripts += [{\"matches\": [\"$TARGET_SERVER/set_robot\"],\"js\": [\"server.js\",\"global.js\",\"emns.js\"]}]" $TARGET_FILE  |sponge $TARGET_FILE 


if [ $DEV_BUILD -eq 1 ]; then
jq '.permissions += ["http://localhost:5000/set_robot"]' $TARGET_FILE  |sponge $TARGET_FILE 
jq '.content_scripts[1].matches += ["http://localhost:5000/set_robot"]' $TARGET_FILE  |sponge $TARGET_FILE 
export RELEASE_TYPE="dev"
else
export RELEASE_TYPE="prod"
fi

#change production server URL
echo "var BASE_URL=\"https://conso-api.vod-prime.space\";" > $TARGET_FOLDER/server.js

cd $TARGET_FOLDER 

zip -qr ../$APP_NAME_ESCAPED-$APP_VERSION-$RELEASE_TYPE.zip *
cd .. && google-chrome-stable --pack-extension=$(basename $TARGET_FOLDER)|true

