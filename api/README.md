prerequisite
=======

installing all prerequisites: flask, sqlacodegen, docker, docker-compose

```bash
	#python dependencies
	pip install Flask flask-cors flask-migrate flask-sqlalchemy sqlacodegen
        #docker-ce
	wget https://get.docker.com -O get.docker.sh
	sh ./get.docker.sh
        #docker compose
	sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
	sudo chmod +x /usr/local/bin/docker-compose
```


Building
========

```bash
make build-api
```

* generates the python-flask REST API layer from its [openapi specification](http://spec.openapis.org/oas/v3.0.2) in file api-definition.yml

```bash
make build-model
```

* generates the persistence model objects from a live SQL connection specified in the MAKEFILE


