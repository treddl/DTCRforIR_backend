#!/bin/bash
#
# runs ARP scan 
docker exec digital_twin screen -S hmi_ids -X stuff "bash nids_hmi.sh^M"
