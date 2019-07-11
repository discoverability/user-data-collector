.DEFAULT_GOAL := all

MYSQL_URL=mysql+oursql://root@localhost/discoverability 

bootstrap:
	pip install Flask flask-cors flask-migrate flask-sqlalchemy sqlacodegen
	wget https://get.docker.com -O get.docker.sh
	sh ./get.docker.sh


run: clean-model
	export FLASK_APP=sniffer_api.py
	flask db init
	flask db migrate
	flask db upgrade
	flask run

all: clean build

clean: clean-api clean-model

build: build-api build-model

clean-api:
	sudo rm -rf generated

build-api:
	sudo docker run --rm \
  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/api-definition.yml \
  -g python-flask \
  -o /local/generated

build-api-client:
	sudo docker run --rm \
  -v ${PWD}/..:/local openapitools/openapi-generator-cli generate \
  -i /local/api/api-definition.yml \
  -g typescript-jquery \
  -o /local/chrome_extension/generated

build-api-client-ruby:
	sudo docker run --rm \
  -v ${PWD}/..:/local openapitools/openapi-generator-cli generate \
  -i /local/api/api-definition.yml \
  -g ruby \
  -o /local/moviedb

clean-model:
	rm -rf sqlgen
	rm -rf migrations
	rm app/app.db

build-model: clean-model
	mkdir -p sqlgen
	sudo sqlacodegen ${MYSQL_URL} > app/modelsgen.py
	flask db init
	flask db migrate
	flask db upgrade
