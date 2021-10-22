#!/bin/bash
#
# stops all running docker container

## preparation to stop containers gracefully
cd ../../src

## reverses the dsiem directives from .json to .txt
bash deactivate_directives.sh

## quits all running screen sessions in the Docker container 'digital_twin'
# sudo docker exec -it digital_twin bash quit_screens.sh 

## quits the screen 'frontend' in the baselayer VM
screen -X -S frontend quit
screen -X -S api quit

## stop containers
cd ../deployments/docker
sudo docker-compose stop 
echo " removed docker container:"
sudo docker container rm elasticsearch 
echo " removed docker volume:"
sudo docker volume rm docker_es-data 