#!/bin/bash
#
# preps the environment and starts the filling plant

# kill all screens
pkill screen

cd src

# remove logs from previous cyber range execution 
rm ./logs/*.log
rm ./logs/host_vm_screen_logs/*.log
rm ./logs/dt_screen_logs/*.log

# start openvswitch and mininet
service openvswitch-switch start
echo 'running command "mn -c"'
mn -c


# initiates the sqlite database for the physical filling process
echo 'running src/init.py'
screen -dmS init_sqlite_db -L -Logfile ./logs/dt_screen_logs/init_sqlite_db-screen.log python init.py

# runs the main python script run.py
echo 'running src/run.py in screen "main_run"'
screen -dmS main_run -L -Logfile ./logs/dt_screen_logs/main_run-screen.log python run.py 
tail -f /dev/null