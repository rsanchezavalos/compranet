.PHONY: start stop status logs restart nuke

########################################
##            Variables               ##
########################################
SHELL := /bin/bash 
PROJECT_NAME:=compranet
DATA_DIRECTORY :=$(CURDIR)/../data
DOCKER_REGISTRY = localhost:5000
IMAGES = python luigi-worker luigi-server python-selenium
#base python r java luigi-server luigi-worker spark-client hadoop-client
IMAGE_VERSION = 0.1




########################################
##             Control                ##
########################################


start: setup

setup: create up


up: .running

.running:
	# Esto corre en infraestructura
	@docker-compose --project-name ${PROJECT_NAME} up -d
	@touch .running

create: .images_built #.data_built .network_built .infrastructure_built

.service_create:# Create Service if you are in swarm mode -> Node1
	@docker service create --name registry --publish 5000:5000 registry:2

.images_built:
	@for image in $(IMAGES); do \
	    sudo docker build --tag ${DOCKER_REGISTRY}/dpa/$$image:${IMAGE_VERSION} --tag dpa/$$image:latest --tag dpa/$$image:$(IMAGE_VERSION) $$image;done;
	    #sudo docker push ${DOCKER_REGISTRY}/dpa/$$image:$(IMAGE_VERSION); 
	@touch .images_built

.data_built:
	echo ${DATA_DIRECTORY}
	[ -d ${DATA_DIRECTORY} ] && docker volume create --name ${PROJECT_NAME}_store --opt type=none --opt device=${DATA_DIRECTORY} --opt o=bind
	@touch .data_built

.network_built:
	@docker network create --driver overlay --subnet=10.0.9.0/24 --attachable ${PROJECT_NAME}_net
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
