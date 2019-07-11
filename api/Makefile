.DEFAULT_GOAL := all

MYSQL_URL=mysql+oursql://root@localhost/discoverability 


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

clean-model:
	rm -rf sqlgen

build-model: clean-model
	mkdir -p sqlgen
	sudo sqlacodegen ${MYSQL_URL} > sqlgen/models.py
