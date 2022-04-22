#!/bin/bash
ip=$(ip addr show enp1s0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
echo "HOST_IP=$ip" > .env
#uncomment if interface for cyber range is known to retrieve ip address automatically

# stop docker containers and remove legacy containers and volumes
docker-compose stop 
echo " removed docker container:"
sudo docker container rm elasticsearch 
echo " removed docker volume:"
sudo docker volume rm docker_es-data 
rm ./logs/*.log

# restart docker containers
docker-compose up -d
# restart docker containers and force build when changes have occured 
#docker-compose up -d --build
# note on the start process:
# docker-compose up automatically runs /build/digital_twin/start.sh as this is the start command (CMD) in the Dockerfile of the digital_twin container

pkill screen
# imports the kibana-based dashboard
#echo 'Stopping legacy kibana-dashboard import screen session'
#screen -X -S kbndashboard-import quit
screen -dmSL main bash ./kbndashboard-import.sh localhost ./../kibana/dashboard-siem.json


# stop and restart the API
#echo 'Stopping legacy api screen session'
#screen -X -S api quit
cd ./../../src/pyrest
#ip_vm=$(cat .env | grep HOST_IP= | cut -d '=' -f2)
#screen -X -S api -Logfile python api.py  
screen -dmSL main python api.py


# stop and restart the frontend
cd ./../../../DTCRforIR_frontend
#rm frontend-screen.log
#echo 'Stopping legacy frontend screen session'
#screen -X -S frontend quit
#screen -dmSL main npm run serve
serve -s -n -l 7080 dist

