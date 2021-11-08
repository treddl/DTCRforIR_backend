"""
hids_plc1.py

Simulates host intrusion detection system (HIDS) running on PLC1.

Continually sniffs network traffic for ICMP and ARP packets.

Logs all ICMP packets with func icmp_parse().

Logs all ARP packets with func arp_parse().

Logs warning for potential ARP spoofing with func check_arp_spoof().

"""

from scapy.all import *
from utils import HMI_ADDR, HMI_MAC, PLC1_ADDR, PLC1_MAC, PLC2_ADDR, PLC2_MAC, PLC3_ADDR, PLC3_MAC, ATTCKR_ADDR, ATTCKR_MAC
import logging
import time

global known_mac_adresses
# represents baseline IP-MAC address mapping
known_mac_adresses={HMI_ADDR: HMI_MAC, 
                    PLC1_ADDR: PLC1_MAC, 
                    PLC2_ADDR: PLC2_MAC, 
                    PLC3_ADDR: PLC3_MAC,
                    ATTCKR_ADDR: ATTCKR_MAC}


# set directory and format of logs 
logging.basicConfig(filename='logs/hids_plc1.log',format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
## note: here argumet <message> equals string variable <log> as defined in functions icmp_parse() and arp_parse()


# checks for ARP spoofing
def check_arp_spoof(pkt, ip_src, ip_dst, mac_src):
    
    ip_src = ip_src
    ip_dst = ip_dst
    
    # save source MAC address from packet
    mac_src = mac_src
    
    #log an ARP spoof warning if the current ARP frame's source MAC address does not match the baseline IP-MAC address mapping
    if (known_mac_adresses[ip_src] != mac_src):
        log="%(PLC1_ADDR)s %(PLC1_ADDR)s "%{"PLC1_ADDR": PLC1_ADDR}+"ARP-SPOOF WARNING:: "+mac_src+" does not match known "+ known_mac_adresses[ip_src]
        
        print(log)
        # log ARP spoof warning in format
        # WARNING 11/04/2021 08:22:33 10.0.0.1 10.0.0.1 ARP-SPOOF WARNING:: 00:00:00:00:00:05 does not match known 00:00:00:00:00:03
        logging.warning(log)


# log all ARP messages
def arp_parse(pkt):

    ip_src = pkt[ARP].psrc
    ip_dst = pkt[ARP].pdst
    mac_src = pkt[ARP].hwsrc
    
    if (ip_src == PLC1_ADDR or ip_dst == PLC1_ADDR):
        # check ARP operations/message type
        if (pkt[ARP].op == 1):
            arp_op="ARP-REQUEST"
            summary="Request: %(srcip)s is asking about %(dstip)s" %{"srcip": ip_src, "dstip": ip_dst}
            log="%(srcip)s %(dstip)s %(arp_op)s:: %(summary)s" %{"srcip": ip_src, "dstip": ip_dst, "arp_op": arp_op, "summary": summary}

        elif (pkt[ARP].op == 2):
            arp_op="ARP-REPLY"
            summary="*Reply: %(srcip)s has MAC address %(srcmac)s" %{"srcip": ip_src, "srcmac": mac_src}
            log="%(srcip)s %(dstip)s %(arp_op)s:: %(summary)s" %{"srcip": ip_src, "dstip": ip_dst, "arp_op": arp_op, "summary": summary}
            check_arp_spoof(pkt, ip_src, ip_dst, mac_src)
        else:
            arp_op="ARP-OTHER"
            #check_arp_spoof(pkt, ip_src, ip_dst, mac_src)
            log="%(srcip)s %(dstip)s %(arp_op)s:: %(summary)s" %{"srcip": ip_src, "dstip": ip_dst, "arp_op": arp_op, "summary": pkt.summary()}

        print(log)
        # log ARP messages in format:
        # INFO 11/04/2021 08:22:42 10.0.0.3 10.0.0.1 ARP-REPLY:: Ether / ARP is at 00:00:00:00:00:03 says 10.0.0.3
        logging.info(log)

        
    #TODO: can be deleted if no firewall/NIDS runs on the HMI
    #check for ARP packets produced by the NIDS running on the HMI
    #this prevents looging the NIDS/firewall running on the HMI
    #if ARP packets have neither the source nor destination IP address of the HMI, then print the ARP log 
    #if (ip_dst != "10.0.0.4") and (ip_src != "10.0.0.4"):

        

# log all ICMP messages
def icmp_parse(pkt):
    
    # save source and destination IP addresses of ICMP packet
    ip_src = pkt[IP].src
    ip_dst = pkt[IP].dst
    
    # check ICMP message type
    if (pkt[ICMP].type == 0):
        icmp_type="ICMP-REPLY"
    elif (pkt[ICMP].type == 8):
        icmp_type="ICMP-REQUEST"
    else:
        icmp_type="ICMP-OTHER"
            
    
    log="%(srcip)s %(dstip)s %(icmp_type)s:: %(summary)s" %{"srcip": ip_src, "dstip": ip_dst, "icmp_type": icmp_type, "summary": pkt.summary()}
    print(log)
    
    # log ICMP messages in format:
    # INFO 11/04/2021 08:27:55 10.0.0.5 10.0.0.1 ICMP-REQUEST:: Ether / IP / ICMP 10.0.0.5 > 10.0.0.1 echo-request 0
    logging.info(log)   
    

# parse all provided ICMP and ARP packets    
def tcp_parse(pkt):
    
    protocol_id=pkt.type
    
    # check for packet type
    ## if ARP then call func arp_parse()
    if protocol_id==2054: #protocol is arp
        arp_parse(pkt)          
    ## if ICMP then call func icmp_parse()
    elif protocol_id==2048: #protocol is icmp
        icmp_parse(pkt)
        
    #pkt.show()
    #MACs: pkt.src, pkt.dst
        

# constnatly sniff network traffic and call func tcp_parse() for each sniffed ICMP or ARP packet
pkts = sniff(filter="icmp or arp",prn=lambda x: tcp_parse(x))

# notes
# filter: Use standard tcpdump/libpcap syntax, e.g., "tcp and host 64.233.167.99 and port 80"
# iface: specifies the interface to be used to sniff

# legacy testing
#sniff(offline="tcpdump.pcap", prn=check_mitm(), filter='tcp or udp')
#pkts = sniff(offline="tcpdump.pcap",prn = check_mitm())
