.PHONY : bump-%
WS_CLIENT_ID=121069493888-b7jbd2gvgulr5pargfnmig0as5h8bicm.apps.googleusercontent.com
WS_API_KEY=AIzaSyDD-Ryao8nyshEC3J7YkakOVDFo334gaIg
TARGET_SERVER=https://conso-api.vod-prime.space
APP_NAME=DiscoSorbonne
DEV_BUILD=0
VERSION := $(shell jq ".version" ./manifest.master)

clean:
	rm -rf build

bootstrap: clean
	mkdir -p build/$(APP_NAME)-prod
	cp -r extension_code/* build/$(APP_NAME)-prod
	mkdir -p build/$(APP_NAME)-dev
	cp -r extension_code/* build/$(APP_NAME)-dev

bump-%:
	$(eval VERSION_NEW :=$(shell ./ext_mgr.py $(VERSION) --$(word 2,$(subst -, ,$@))))
	

update-version-%: bootstrap bump-% 
	echo "updating to version $(VERSION_NEW)" 
	./release.sh "build/$(APP_NAME)-prod" "$(APP_NAME)" "$(VERSION_NEW)" "$(TARGET_SERVER)" "0"
	./release.sh "build/$(APP_NAME)-dev" "$(APP_NAME)" "$(VERSION_NEW)" "$(TARGET_SERVER)" "1"
