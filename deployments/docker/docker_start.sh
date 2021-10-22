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
screen -dmS kibana_dashbaord_import -L -Logfile kibana_dashbaord_import-screen.log bash kbndashboard-import.sh localhost ../kibana/dashboard-siem.json

# reverts the dsiem correlation directives .json to .txt
cd ./../../src
screen -dmS run_deactivate_directives -L -Logfile ./logs/host_vm_screen_logs/run_deactivate_directives-screen.log bash deactivate_directives.sh 

# restarts the API
cd pyrest
screen -dmS api -L -Logfile ../logs/host_vm_screen_logs/api-screen.log python api.py 


# restarts the frontend
cd ./../../../DTCRforIR_frontend
rm frontend-screen.log
screen -dmS frontend -L -Logfile frontend-screen.log npm run serve 
