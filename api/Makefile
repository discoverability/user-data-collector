.DEFAULT_GOAL := all

MYSQL_URL=mysql+oursql://root@localhost/discoverability 

bootstrap:
	pip install Flask flask-cors flask-migrate flask-sqlalchemy sqlacodegen
	wget https://get.docker.com -O get.docker.sh
	sh ./get.docker.sh

init:
	cd app &&	FLASK_APP=app.main flask db init && 	FLASK_APP=app.main flask db migrate &&	FLASK_APP=app.main flask db upgrade 
run: 
	cd app && 	FLASK_APP=app.main flask db migrate && FLASK_APP=app.main flask db upgrade &&	LOG_LEVEL=debug FLASK_APP=app.main flask run 

run-prod:
	cd app && APP_ENV=production FLASK_APP=app.main flask run 
all: clean build

clean: 
	rm -rf ./app.db
	rm -f app/app.db
	rm -rf ./app/migrations
	rm -rf migrations
	rm -rf ./app/app/migrations
	rm -rf ./app/app/app.db


build: build-api build-model

docker:
	docker build . -t discoverability/conso-api 
docker-run:
	docker run -e LOG_LEVEL="debug" -p 80:80 discoverability/conso-api 
compose-run:
	docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml up -d
docker-push:
	docker push discoverability/conso-api

clean-model:
	rm -rf sqlgen
	rm -rf migrations
	rm -rf app/app.db

run-prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
stop-prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml down 
