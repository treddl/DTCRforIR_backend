#!/bin/bash
#
# starts docker containers 

#ip=$(ip addr show enp1s0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
#echo "HOST_IP=$ip" > .env
#uncomment if interface for cyber range is known to retrieve ip address automatically

#restart docker containers
pkill screen
docker-compose stop 
docker-compose up -d --build

screen -dmSL kibana_dashbaord_import /bin/bash kbndashboard-import.sh localhost ../kibana/dashboard-siem.json

#restart api
cd ./../../src
screen -dmSL run_deactivate_directives bash deactivate_directives.sh -Logfile
cd pyrest
screen -dmSL run_api python api.py -Logfile

cd ./../../../DTCRforIR_frontend
screen -dmSL frontend npm run serve -Logfile