export TARGET_FOLDER="$1"
export APP_NAME="$2"
export APP_VERSION="$3"
export TARGET_SERVER="$4"
export DEV_BUILD="$5"



cp manifest.master $TARGET_FOLDER/manifest.json 


jq ".version = \"$APP_VERSION\"" $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
jq ".name= \"$APP_NAME\"" $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
jq 'del(.content_scripts)' $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
jq '.content_scripts += [{ "matches": ["https://*.netflix.com/*"], "js": ["global.js","netflix_lib.js","netflix.js"]}]' $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
jq ".content_scripts += [{\"matches\": [\"$TARGET_SERVER/set_robot\"],\"js\": [\"global.js\",\"emns.js\"]}]" $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 


if [ $DEV_BUILD -eq 1 ]; then
jq '.permissions += ["http://localhost:5000/set_robot"]' $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
jq '.content_scripts[1].matches += ["http://localhost:5000/set_robot"]' $TARGET_FOLDER/manifest.json  |sponge $TARGET_FOLDER/manifest.json 
export RELEASE_TYPE="dev"
else
export RELEASE_TYPE="prod"
fi


cd $TARGET_FOLDER && zip -r ../$APP_NAME-$APP_VERSION-$RELEASE_TYPE.zip *