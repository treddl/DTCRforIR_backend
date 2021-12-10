from utils import PLC1_ADDR, PLC2_ADDR, PLC3_ADDR, HMI_ADDR, ATTCKR_ADDR
from scapy.all import *
import logging
import time

# no use of this script in my cyber range

"""
Implements a scpay-based network intrusion detection system (NIDS).

The NIDS function is achieved by performing ARP scans on the network.


"""


def arp_scan():
    # sets log format 
    logging.basicConfig(filename='logs/nids_hmi.log',format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
    
    # list of known hosts
    known_hosts=[PLC1_ADDR, PLC2_ADDR, PLC3_ADDR, HMI_ADDR, ATTCKR_ADDR]
    
    # create ARP frame
    arp = ARP(pdst="10.0.0.4/24")
    
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # stack them
    packet = ether/arp

    # performing ARP scan in broadcast
    result = srp(packet, timeout=3, verbose=0)[0]

    # a list of clients, we will fill this in the upcoming loop
    clients = []
    
    for sent, received in result:
        clients.append(received.psrc)
     
    for client in clients:
        log="%(HMI_ADDR)s %(HMI_ADDR)s test-warning ids_hmi:: WARNING: HMI (10.0.0.4) successfully reached host: %(client)s" %{"HMI_ADDR": HMI_ADDR, "client": client}
        print(log)
        logging.warning(log)
        time.sleep(3)

        
arp_scan()

"""
while True:
    arp_scan()
    time.sleep(30)
"""