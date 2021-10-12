#!/bin/bash

cd src
ls
service openvswitch-switch start
echo 'running command "mn -c"'
mn -c
rm ./logs/plc1.log
rm ./logs/plc2.log
rm ./logs/plc3.log
rm ./logs/tcpdump.log
rm ./logs/firewall.log

# initiates the sqlite database for the physical filling process
echo 'running src/init.py'
python init.py

# runs the main python script run.py
echo 'running src/run.py in screen "main_run"'
screen -dmSL main_run python run.py
tail -f /dev/null
