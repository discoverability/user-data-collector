set -x 

export TARGET_FOLDER="$(printf %q "$1")"
export APP_NAME="$2"
export APP_VERSION="$3"
export TARGET_SERVER="$4"
export DEV_BUILD="$5"

DIR="$(dirname "$0")"

export TARGET_FILE="$TARGET_FOLDER/manifest.json"
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

cd $TARGET_FOLDER && zip -q -r ../$APP_NAME-$APP_VERSION-$RELEASE_TYPE.zip *
cd .. && google-chrome-stable --pack-extension=$(basename $TARGET_FOLDER)|true
echo $DIR/$TARGET_FOLDER/../$APP_NAME-$APP_VERSION-$RELEASE_TYPE.zip
