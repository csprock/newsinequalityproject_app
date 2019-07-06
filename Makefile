

#### Application Settings #####
COMPOSE_APP := docker-compose-app.yml
BUILD_CACHE := --no-cache
DB_VOLUME := nip_app_metadata


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
