#!/bin/bash
#
# starts the MitM attack via ARP spoofing
echo 'run mitm_attack_start.sh'


docker exec digital_twin screen -S attacker_mitm -X stuff "bash attack/mitm_attack.sh^M"

# notes
## docker exec digital_twin: runs the arguments that follow in inside the digtial_twin container
## screen -S attacker -X: runs the following command in the detached screen session named 'attacker'
## stuff "bash attack/mitm_attack.sh^M": argument/command that is run inside the screen session named 'attacker', '^M' corrensponds to hitting enter on the given input 
