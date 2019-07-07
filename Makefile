

COMPOSE_APP := docker-compose-app.yml
BUILD_CACHE := --no-cache
DB_VOLUME := nip_app_metadata

APP_SERVICE := app
DB_SERVICE := db
PROXY_SERVICE := nginx

#################################
####### Run Application #########
#################################


## build
build:
	docker-compose -f ${COMPOSE_APP} build ${BUILD_CACHE}

## run-app
run-app:
	docker-compose -f ${COMPOSE_APP} up -d

## run-app-no-detach
run-app-no-detach:
	docker-compose -f ${COMPOSE_APP} up

## stop-app
stop-app:
	docker-compose -f ${COMPOSE_APP} down --remove-orphans

## logs
logs:
	docker-compose -f ${COMPOSE_APP} logs

## clean
clean:
	docker-compose -f ${COMPOSE_APP} down --remove-orphans --rmi all

## clean-data
clean-data:
	docker volume rm ${DB_VOLUME}

## clean-all
clean-all: clean clean-data

#### database commands #####

## init-db
init-db:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask db init

## migrade-db
migrate-db:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask db migrate
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask db upgrade

## create-author
create-author:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata create_author --firstname $(firstname) --lastname $(lastname) --email $(email) --handle $(handle)

## create-post
create-post:
ifeq ($(url), )
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata create_post --title $(title) --author_id $(author_id) --year $(year) --month $(month) --day $(day) --header_pic $(header_pic)
else
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata create_post --title $(title) --author_id $(author_id) --year $(year) --month $(month) --day $(day) --url $(url) --header_pic $(header_pic)
endif

## delete-author
delete-author:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata delete_author --author_id $(author_id)

## delete-post
delete-post:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata delete_post --post_id $(post_id)