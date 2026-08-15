IMAGE_NAME := asep_python_311:latest
SQLITE_IMAGE := keinos/sqlite3
DATETIME := $(`date -j '+%Y%m%d%H%M'`)

DOCKER_RUN := docker run -it --rm \
	--network asep_backend \
	-v ${PWD}/:/opt/asep \
	-w "/opt/asep" \
	${IMAGE_NAME}

build:
	@echo "build"
	docker build \
		-f ./Dockerfile \
		-t ${IMAGE_NAME} .

ssh:
	${DOCKER_RUN} /bin/bash

import.qualifications:
	@echo "${YEAR}" "${SPEC}" "${FILE}"
	${DOCKER_RUN} python /opt/asep/src/import_qualifications.py "${SPEC}" "${FILE}" "${YEAR}"

import.positions:
	@echo "${YEAR}" "${PHASE}" "${FILE}"
	${DOCKER_RUN} python /opt/asep/src/import_anaplirotes.py "${YEAR}" "${PHASE}" "${FILE}"

run.qualifications.sh:
	./scripts/2ge_2026.sh

# run.anaplirotes.2023-24:
# ${DOCKER_RUN} python /opt/asep/src/import_anaplirotes.py "2023-24" "A" "anaplirotes/2023-24/a_fasi/Προσλήψεις_Γενικής_ΔΕ_20230901_int.xls"
# ${DOCKER_RUN} python /opt/asep/src/import_anaplirotes.py "2023-24" "B" "anaplirotes/2023-24/b_fasi/Προσλήψεις_Γενικής_ΔΕ_20231003_int.xls"
# ${DOCKER_RUN} python /opt/asep/src/import_anaplirotes.py "2023-24" "C" "anaplirotes/2023-24/c_fasi/Προσλήψεις_Γενικής_ΔΕ_20231128_int.xls"

run.db: db.run

phpmyadmin:
	open http://localhost:8081

MYSQL_RUN := docker compose -f ./docker-compose.yml
db.run:
	${MYSQL_RUN} up -d
db.rm:
	${MYSQL_RUN} rm -f
db.logs:
	${MYSQL_RUN} logs
db.stop:
	${MYSQL_RUN} stop
db.down:
	${MYSQL_RUN} down
db.pull:
	${MYSQL_RUN} pull

db.update: \
	db.pull \
	db.stop \
	db.rm \
	db.run

db.cleanup: db.stop
	docker container rm db pma
	docker volume rm asep_dbdata

db.dump:
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db .dump > /db/dump.sql"
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db .schema > /db/schema.sql"
db.restore:
	${SQLITE_RUN} sh -c "sqlite3 /db/database.db < /db/dump.sql"

convert:
	find . -type f -name "*.xlsx" -print -execdir /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to xls "{}" \;
	find . -type f -name "*.xlsx" -print -execdir rm -rf "{}" \;

# PYTHON VENV
venv.create:
	python3 -m venv "${PWD}/venv"

venv.pip:
	source "${PWD}/venv/bin/activate" && \
	pip install --upgrade pip && \
	pip install -r requirements.txt


# ALEMBIC - START
migrate: alembic.migrate
alembic.init:
	${DOCKER_RUN} alembic init alembic

alembic.initial_migration:
	${DOCKER_RUN} alembic revision --autogenerate -m "Initial migration"

alembic.migrate:
	${DOCKER_RUN} alembic upgrade head

alembic.downgrade:
	${DOCKER_RUN} alembic upgrade head

alembic.create_migration:
	${DOCKER_RUN} alembic revision --autogenerate -m "${message}"

# ALEMBIC - STOP
