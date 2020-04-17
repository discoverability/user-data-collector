.DEFAULT_GOAL := all

MYSQL_URL=mysql+oursql://root@localhost/discoverability 

bootstrap:
	pip install Flask flask-cors flask-migrate flask-sqlalchemy sqlacodegen
	wget https://get.docker.com -O get.docker.sh
	sh ./get.docker.sh

init:
	export FLASK_APP=./sniffer_api.py
	flask db init 
	flask db migrate 
	flask db upgrade 
run: 
	export FLASK_APP=./sniffer_api.py
	flask db migrate 
	flask db upgrade 
	flask run 

all: clean build

clean: clean-model

build: build-api build-model


clean-model:
	rm -rf sqlgen
	rm -rf migrations
	rm -rf app/app.db

