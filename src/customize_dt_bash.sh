#!/bin/bash
#
# create custom bash inside the digital_twin container

cat src/custom_dt_bash.txt >> /root/.bashrc
#sleep 3
source /root/.bashrc
#sleep 3