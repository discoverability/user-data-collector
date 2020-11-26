VERSION=$(shell git describe --tags)
VERSION_MAJOR=$(shell git describe --tags|sed -rn 's/([0-9]+)\..*/\1/p')
VERSION_MAJOR_MINOR=$(shell git describe --tags|sed -rn 's/([0-9]+\.[0-9]+)\..*/\1/p')
docker-build-testing:
	docker build . -t discoverability/conso-api:testing
docker-push-testing:
	docker push discoverability/conso-api:testing
docker-build-release:
	docker build . -t discoverability/conso-api:$(VERSION)
docker-push-release:
	docker tag discoverability/conso-api:$(VERSION) discoverability/conso-api:$(VERSION_MAJOR)
	docker tag discoverability/conso-api:$(VERSION) discoverability/conso-api:$(VERSION_MAJOR_MINOR)
	docker push discoverability/conso-api:$(VERSION)
	docker push discoverability/conso-api:$(VERSION_MAJOR)
	docker push discoverability/conso-api:$(VERSION_MAJOR_MINOR)


