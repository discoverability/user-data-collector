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

docker:
	docker build . -t discoverability/conso-api 
docker-run:
	docker run -e LOG_LEVEL="debug" -p 80:80 discoverability/conso-api 

docker-push:
	docker push discoverability/conso-api

clean-model:
	rm -rf sqlgen
	rm -rf migrations
	rm -rf app/app.db

