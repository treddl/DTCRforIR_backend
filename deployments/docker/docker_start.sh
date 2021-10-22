#!/bin/bash
#
# starts docker containers 

#ip=$(ip addr show enp1s0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)
#echo "HOST_IP=$ip" > .env
#uncomment if interface for cyber range is known to retrieve ip address automatically

#restart docker containers
pkill screen
docker-compose stop 
docker-compose up -d 


# imports the kibana-based dashboard
screen -dmSL kibana_dashbaord_import /bin/bash kbndashboard-import.sh localhost ../kibana/dashboard-siem.json

# reverts the dsiem correlation directives .json to .txt
cd ./../../src
rm ./logs/run_deactivate_directives-screen.log
screen -dmSL run_deactivate_directives bash deactivate_directives.sh -Logfile ./logs/run_deactivate_directives-screen.log

# restarts the API
cd pyrest
rm ../logs/api-screen.log
screen -dmSL api python api.py -Logfile ../logs/api-screen.log

# restarts the frontend
cd ./../../../DTCRforIR_frontend
rm frontend-screen.log
screen -dmSL frontend npm run serve -Logfile frontend-screen.log