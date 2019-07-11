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


Code generation
========

We rely on [OpenAPIs code generation](http://openapis.org/) and sql reverse engineering to create back-end code for rest APIs and persistence.

python rest api
-----------------

```bash
make build-api
```

* generates the python-flask REST API layer from its [openapi specification](http://spec.openapis.org/oas/v3.0.2) in file api-definition.yml


python persistence models
-------------------------
```bash
make build-model
```

* generates the persistence model objects from a live SQL connection specified in the MAKEFILE


Javascript client API
------------------

```bash 
make build-api-client
```

* generates the typescript-jquery client for the API

Ruby client API
-------------------

```bash 
make build-api-client-ruby
```
* generates the ruby client for the API