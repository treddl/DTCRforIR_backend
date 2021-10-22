#!/bin/bash
#
# greps IP address of the cyber range host (i.e., the IP address of the Ubuntu VM)

cat ./../../deployments/docker/.env | grep HOST_IP= | cut -d '=' -f2
