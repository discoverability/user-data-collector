export PATH := .:$(PATH)
export DRIVER_URL := https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip

bootstrap:
	rm -f driver.zip
	wget $(DRIVER_URL) -O driver.zip
	unzip -o -d . driver.zip
	sudo bundle install
	cd ../chrome_extension && $(MAKE) build
	cp ../chrome_extension/build/DiscoSorbonne-prod.crx chrome_extension.crx
clean:
	rm -f ./chrome_extension.crx

run: 
	./runall.sh
