#!/bin/bash
#
# preps the environment and starts the filling plant

# removes all dead screens
#echo 'wiping and quitting dead and detached screens'
#screen -wipe
#screen -ls | grep '(Detached)' | awk '{print $1}' | xargs -I % -t screen -X -S % quit
pkill screen

cd src

# remove logs from previous cyber range execution 
rm ./logs/*.log

# start openvswitch and mininet
service openvswitch-switch start
echo 'running command "mn -c"'
mn -c


# initiates the sqlite database for the physical filling process
echo 'running src/init.py'
python init.py

# runs the main python script run.py
echo 'running src/run.py in screen "main_run"'
screen -dmSL main_run python run.py -Logfile ./logs/main_run-screen.log
tail -f /dev/null
