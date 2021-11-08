#!/bin/bash
#
# stops all running docker container

## preparation to stop containers gracefully


## reverses the dsiem directives from .json to .txt
#cd ../../src
#bash deactivate_directives.sh
#cd ../deployments/docker/

## quits the screen 'frontend' in the cyber range host VM
screen -X -S frontend quit
screen -X -S api quit

## stop containers
sudo docker-compose stop 
echo " removed docker container:"
sudo docker container rm elasticsearch 
echo " removed docker volume:"
sudo docker volume rm docker_es-data 