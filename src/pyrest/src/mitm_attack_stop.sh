#!/bin/bash
#
# stops the MitM attack via ARP spoofing
echo 'run mitm_attack_stop.sh'
docker exec digital_twin screen -S attacker_mitm -X stuff "^C"