.PHONY: start stop status logs restart nuke

########################################
##            Variables               ##
########################################
SHELL := /bin/bash 
PROJECT_NAME:=dummy
DATA_DIRECTORY:=$(CURDIR)/../data

IMAGES = base python r java luigi-server luigi-worker spark-client hadoop-client
IMAGE_VERSION:=0.1

########################################
##             Control                ##
########################################


start: setup

setup: create up


up: .running

.running:
	@docker-compose --project-name ${PROJECT_NAME} up -d
	@touch .running


create: .data_built .network_built .images_built


.images_built:
	@for image in $(IMAGES) ; do \
	 	 docker build --tag dpa/$$image:$(IMAGE_VERSION) --tag dpa/$$image:latest $$image ; \
	 done
	@touch .images_built

.data_built:
	echo ${DATA_DIRECTORY}
	[ -d ${DATA_DIRECTORY} ] && docker volume create --name ${PROJECT_NAME}_store --opt type=none --opt device=${DATA_DIRECTORY} --opt o=bind
	@touch .data_built

.network_built:
	@docker network create ${PROJECT_NAME}_net
	@touch .network_built


.infrastructure_built:
	@docker-compose --project-name ${PROJECT_NAME} build
	@touch .infrastructure_built


register_images:
	@echo TODO 


stop:
	docker-compose --project-name ${PROJECT_NAME} stop
	@rm -rf .running || true

status:
	@docker-compose --project-name ${PROJECT_NAME} ps

logs:
	@docker-compose --project-name ${PROJECT_NAME} logs


restart: stop clean start status

clean: stop clean_containers clean_data clean_network

nuke: clean clean_images

clean_containers:
	@docker-compose --project-name ${PROJECT_NAME} down --volumes --remove-orphans
	@docker-compose --project-name ${PROJECT_NAME} rm -f
	@rm -rf .infrastructure_built || true

clean_images:
	@docker images -a | grep "dpa" | awk  '{print $1 "\:" $2}' | xargs docker rmi
	@rm -rf .images_built || true

clean_data:
	@docker volume rm ${PROJECT_NAME}_store
	@rm -rf .data_built || true

clean_network: stop
	@docker network rm ${PROJECT_NAME}_net
	@rm -rf .network_built || true
