#!/bin/bash
#
# customizes the bash commands available from inside the docker container 'digital_twin'
echo "alias screenls='screen -ls'" >> /root/.bashrc
echo "alias screenr='screen -r '$1'" >> /root/.bashrc
echo "screenq () {\nscreen -X -S '$1' quit\n}" >> /root/.bashrc
#echo "alias ALIAS_NAME='COMMAND'" >> .bashrc
source /root/.bashrc
