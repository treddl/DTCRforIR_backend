from utils import PLC1_ADDR, PLC2_ADDR, PLC3_ADDR, HMI_ADDR
from scapy.all import *
import logging
import time

# no use of this script in my cyber range

"""
Implements a scpay-based network intrusion detection system (NIDS).

The NIDS function is achieved by performing ARP scans on the network.

The ARP scan reveals if there's an unknown host in the network.
"""


def arp_scan():
    # list of known hosts, i.e., all hosts except for the Attacker
    known_servers=[PLC1_ADDR, PLC2_ADDR, PLC3_ADDR, HMI_ADDR]
    
    
    # NB: this script assumes there's an attacker on host 10.0.0.4
    
    # IP Address for the destination
    target_ip = "10.0.0.4/24"
    
    # create ARP packet
    arp = ARP(pdst=target_ip)
    
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # stack them
    packet = ether/arp

    result = srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []

    # sets log format 
    logging.basicConfig(filename='logs/nids_hmi.log',format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
    
    for sent, received in result:
        clients.append(received.psrc)
     
    for client in clients:
        if client not in known_servers:
            print("possible attacker: ",client)
            log=HMI_ADDR+" %(ATTACKER_ADDR)s FIREWALL-WARNING: Unkown IP address in network: %(ATTACKER_ADDR)s" %{"ATTACKER_ADDR": client}
            print(log)
            logging.warning(log)
            
while True:
    arp_scan()
    time.sleep(30)