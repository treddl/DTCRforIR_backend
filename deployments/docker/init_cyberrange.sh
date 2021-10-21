#!/bin/bash
#
# initial script to build and start the cyber range

# updates the ownership of all .yml config files to root
chown root $(find conf/filebeat/ conf/filebeat-es/ -name "*.yml")

# kills all running screens
pkill screen

# requests and saves the user to provide the IP address for deploying the cyber range
echo -n "Enter the Hostname or IP Address where the cyber range will be deployed:"
read ip
echo "HOST_IP=$ip" > .env 

# starts the cyber range
bash docker_start.sh
