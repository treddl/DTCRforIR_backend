#!/bin/bash
#
# sets up the host of the cyber range with necessary dependencies 
# in most cases, the host of the cyber range is an Ubuntu-based VM
sudo apt install -y screen && 
sudo apt install -y python3 &&
sudo apt install -y python3-pip &&
pip3 install flask flask-cors
