"""
Simulates a host intrusion detection system (HIDS) running on the given host.

Given hosts may be 

Continually sniffs network traffic for ICMP and ARP packets.

Logs captured ICMP packets to and from given host with func icmp_parse().

Logs captured ARP frames to and from given host with func arp_parse().

Logs warning of potential ARP spoofing with func check_arp_spoof().

"""

import sys
import time
import logging
from scapy.all import *
from utils import HMI_ADDR, HMI_MAC, PLC1_ADDR, PLC1_MAC, PLC2_ADDR, PLC2_MAC, PLC3_ADDR, PLC3_MAC, ATTCKR_ADDR, ATTCKR_MAC


global hids_host
global system_name 
global known_mac_adresses
global known_hosts
global host

# represents baseline IP-MAC address mapping
known_mac_adresses={HMI_ADDR: HMI_MAC, 
                    PLC1_ADDR: PLC1_MAC, 
                    PLC2_ADDR: PLC2_MAC, 
                    PLC3_ADDR: PLC3_MAC,
                    ATTCKR_ADDR: ATTCKR_MAC}


# check for ARP spoofing
def check_arp_spoof(pkt, ip_src, ip_dst, mac_src):
    
    pkt = pkt
    ip_src = ip_src
    ip_dst = ip_dst
    mac_src = mac_src
    
    #log warning if the current ARP frame's src MAC addr does not match the baseline IP-MAC addr mapping
    if (known_mac_adresses[ip_src] != mac_src):
        log=hids_host+' '+hids_host+' '+'ARP-spoof-WARNING '+system_name+':: WARNING: IP (' +ip_src+ ') claimes to have MAC (' +mac_src+"); this does not match known MAC "+known_mac_adresses[ip_src]
        print(log)
        logging.warning(log)
        
        
def log_icmp_scan(ip_src):
    add_info = host.upper()+ ' (' +hids_host+') successfully reached host:'+ ip_src
    log=hids_host+' '+hids_host+' test-warning  '+system_name+':: WARNING: ' + add_info
    print(log)
    logging.warning(log)


# log ARP messages
def arp_parse(pkt):

    ip_src = pkt[ARP].psrc
    ip_dst = pkt[ARP].pdst
    mac_src = pkt[ARP].hwsrc
    
    # capture only ARP frames from or directed at the present host
    if (ip_src == hids_host or ip_dst == hids_host):
        if (pkt[ARP].op == 1):
            arp_op="ARP-request"
            add_info=arp_op+': '+str(ip_src)+'('+mac_src+')'+" is asking about "+str(ip_dst)            
            log=str(ip_src)+' '+str(ip_dst)+' '+arp_op+' '+system_name+':: INFO: '+add_info
        elif (pkt[ARP].op == 2):
            arp_op="ARP-reply"
            add_info=arp_op+': '+str(ip_src)+" has MAC address "+mac_src
            log=str(ip_src)+' '+str(ip_dst)+' '+arp_op+' '+system_name+':: INFO: '+add_info
            check_arp_spoof(pkt, ip_src, ip_dst, mac_src)
        else:
            arp_op="ARP-OTHER"
            #check_arp_spoof(pkt, ip_src, ip_dst, mac_src)
            add_info = str(pkt.summary())
            log=str(ip_src)+' '+str(ip_dst)+' '+arp_op+' '+system_name+':: INFO: '+add_info

        print(log)
        logging.info(log)

# log ICMP messages
def icmp_parse(pkt):
    
    ip_src = pkt[IP].src
    ip_dst = pkt[IP].dst
    mac_src = pkt[Ether].src
    
    # capture only ICMP packets from or directed at the present host
    if (ip_src == hids_host or ip_dst == hids_host):
        # check ICMP message type
        if (pkt[ICMP].type == 0):
            icmp_type="ICMP-reply"
            if (system_name == known_hosts[3]):
                log_icmp_scan(ip_src)
        elif (pkt[ICMP].type == 8):
            icmp_type="ICMP-request"
        else:
            icmp_type="ICMP-OTHER"
            
    
    add_info = icmp_type+': '+str(ip_src)+' ('+mac_src+')'+' > '+str(ip_dst)
    log=str(ip_src)+' '+str(ip_dst)+' '+icmp_type+' '+system_name+':: INFO: '+add_info
    print(log)    
    logging.info(log)   
    

# parse all captured ICMP and ARP packets    
def tcp_parse(pkt):
    
    protocol_id=pkt.type
    
    # check for packet type
    if protocol_id==2054: #is arp
        arp_parse(pkt)          
    elif protocol_id==2048: #is icmp
        icmp_parse(pkt)
    
    #uncomment to print the entire packet on SDTOUT
    #pkt.show()
     

host = str(sys.argv[1])
print('Given host name: ', host)
known_hosts = ['plc1', 'plc2', 'plc3', 'hmi', 'attacker']

 
if (str(host) == known_hosts[0]):
    hids_host = PLC1_ADDR
    system_name = 'ids_'+ host
elif (str(host) == known_hosts[1]):
    hids_host = PLC2_ADDR
    system_name = 'ids_'+ host
elif (str(host) == known_hosts[2]):
    hids_host = PLC3_ADDR
    system_name = 'ids_'+ host
elif (str(host) == known_hosts[3]):
    hids_host = HMI_ADDR
    system_name = 'ids_'+ host
elif (str(host) == known_hosts[4]):
    hids_host = ATTCKR_ADDR
    system_name = "ids_work-station"
    host = "work-station"
else:
    raise ValueError('Given host name "'+host+'" does not match list of known hosts: '+ str(known_hosts))

    
hids_host = str(hids_host)    
print('INFO hids_host name is: '+hids_host)
    # set directory and format of logs 
    
print('INFO system_name is: '+system_name)
    
file_name = 'logs/'+system_name+'.log'
print('INFO logs are stored at: '+file_name)

logging.basicConfig(filename=file_name, format='%(levelname)s %(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
## note: here argumet <message> equals string variable <log> as defined in functions icmp_parse() and arp_parse()
# logs ARP spoof warning in format
# WARNING 11/04/2021 08:22:33 10.0.0.1 10.0.0.1 ARP-SPOOF WARNING:: hids_plc1 warns: 00:00:00:00:00:05 does not match known 00:00:00:00:00:03
# logs ARP messages in format:
# INFO 11/04/2021 08:22:42 10.0.0.3 10.0.0.1 ARP-REPLY:: Ether / ARP is at 00:00:00:00:00:03 says 10.0.0.3
# logs ICMP messages in format:
# INFO 11/04/2021 08:27:55 10.0.0.5 10.0.0.1 ICMP-REQUEST:: hids_plc1 captured: ICMP-REQUEST: 10.0.0.5 (00:00:00:00:00:05) > 10.0.0.1
    
# constantly sniff network traffic and call func tcp_parse() for each sniffed ICMP or ARP packet
print('INFO ***'+system_name+' now monitors for ICMP and ARP traffic***')
pkts = sniff(filter="icmp or arp",prn=lambda x: tcp_parse(x))
# notes
# filter: Use standard tcpdump/libpcap syntax, e.g., "tcp and host 64.233.167.99 and port 80"
# iface: specifies the interface to be used to sniff