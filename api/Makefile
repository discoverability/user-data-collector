clean:
	sudo rm -rf generated

build:
	sudo docker run --rm \
  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
  -i /local/api-definition.yml \
  -g python-flask \
  -o /local/generated
