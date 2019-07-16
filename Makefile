##################################
##### Define resource names ######
##################################

APP_NAME := newsinequalityproject_app

COMPOSE_APP := docker-compose-app.yml
BUILD_CACHE := --no-cache
DB_VOLUME := ${APP_NAME}_app_metadata

APP_SERVICE := app
DB_SERVICE := db
PROXY_SERVICE := nginx

AWS_PUBLIC_IP := 3.219.123.60
AWS_USER := ubuntu
AWS_PUBLIC_KEY := /home/csprock/.ssh/nip-app-dev.pem

# SECRETS_APP := .secrets-app
# SECRETS_DB := .secrets-db
# ENV_APP := app.env

############################################
##### Define file paths and locations ######
############################################

STATIC_DIR := ./app/app/static/blog
STATIC_OTHER_DIR := ./app/app/static/blog/other

REMOTE_STATIC_DIR := /home/ubuntu/newsinequalityproject_app/app/app/static/blog
REMOTE_STATIC_OTHER_DIR := /home/ubuntu/newsinequalityproject_app/app/app/static/blog/other

CONFIG_DIR := ./config
REMOTE_CONFIG_DIR := /home/ubuntu/newsinequalityproject_app/config

TEMPLATE_DIR := ./app/app/templates/blog
REMOTE_TEMPLATE_DIR := /home/ubuntu/newsinequalityproject_app/app/app/templates/blog


#### SCP file copy commands ####

copy-blog-files:
	ssh -i ${AWS_PUBLIC_KEY} ${AWS_USER}@${AWS_PUBLIC_IP} "mkdir ${REMOTE_STATIC_DIR}/post_$(post)"
	scp -i ${AWS_PUBLIC_KEY} -r ${STATIC_DIR}/post_$(post)/* ${AWS_USER}@${AWS_PUBLIC_IP}:${REMOTE_STATIC_DIR}/post_$(post)
	scp -i ${AWS_PUBLIC_KEY} -r ${TEMPLATE_DIR}/post_$(post).html ${AWS_USER}@${AWS_PUBLIC_IP}:${REMOTE_TEMPLATE_DIR}/post_$(post).html

copy-other-files:
	scp -i ${AWS_PUBLIC_KEY} -r ${STATIC_OTHER_DIR}/$(file) ${AWS_USER}@${AWS_PUBLIC_IP}:${REMOTE_STATIC_OTHER_DIR}/$(file)

copy-secrets-file:
	scp -i ${AWS_PUBLIC_KEY} ${CONFIG_DIR}/$(file) ${AWS_USER}@${AWS_PUBLIC_IP}:${REMOTE_CONFIG_DIR}/$(file)


# copy-secrets: copy-secrets-file
# 	copy-secrets-file file=${SECRETS_APP}
# 	copy-secrets-file file=${SECRETS_DB}
# 	copy-secrets-file file=${ENV_APP}

#### app commands ####

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

init-all: init-dir init-db migrate-db


init-dir:
	docker-compose -f ${COMPOSE_APP} run -d ${APP_SERVICE} flask metadata init_directories

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