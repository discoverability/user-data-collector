export PATH := .:$(PATH)
export DRIVER_URL := https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip

bootstrap:
	rm -f driver.zip
	wget $(DRIVER_URL) -O driver.zip
	unzip -o -d . driver.zip
	sudo bundle install
clean:
	rm -f ../chrome_extension.pem
	rm -f ../chrome_extension.crx
	rm -f ./chrome_extension.crx
pack: clean
	cd .. && google-chrome-stable --pack-extension=chrome_extension |true 
	cp ../chrome_extension.crx .

run: pack
	./runall.sh
