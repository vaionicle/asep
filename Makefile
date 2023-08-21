IMAGE_NAME := asep_python_311:latest
SQLITE_IMAGE := keinos/sqlite3

DOCKER_RUN := docker run -it --rm \
	--network asep_backend \
	-v ${PWD}/:/opt/asep \
	-w "/opt/asep" \
	${IMAGE_NAME}

MYSQL_RUN := docker-compose -f ./docker-compose.yml

build:
	@echo "build"
	docker build \
		-f ./Dockerfile \
		-t ${IMAGE_NAME} .

ssh:
	${DOCKER_RUN} /bin/sh

run:
	${DOCKER_RUN} python /opt/asep/src/import.py

extract:
	@echo "extract"


import:
	@echo "Import"

phpmyadmin:
	open http://localhost:8081


db.run:
	${MYSQL_RUN} up -d
db.logs:
	${MYSQL_RUN} logs
db.stop:
	${MYSQL_RUN} stop

db.cleanup:
	docker container rm db pma
	docker volume rm asep_dbdata

db.dump:
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db .dump > /db/dump.sql"
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db .schema > /db/schema.sql"

db.restore:
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db < /db/dump.sql"