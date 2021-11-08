"""
FP run.py

Main script of the filling plant.

Runs the scripts of the filling process, the defense capability and the attack capability.

"""

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.term import makeTerm
from minicps.mcps import MiniCPS
from topo import FPTopo


import sys
from mininet.log import lg, info
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.util import waitListening


import time


class FPCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):
        
        self.name = name
        self.net = net
        
        # start devices
        plc1, plc2, plc3, s1, attacker, hmi = self.net.get('plc1', 'plc2', 'plc3', 's1',  'attacker', 'hmi')
        info("\n***Retrieved hosts:\n")
        info(plc1, plc2, plc3, s1, attacker, hmi)
        
        # start the network
        info( "\n***Start network and ping all:\n" )
        net.start()
        net.pingAll()
        
        
        
        # the FILLING PROCESS 
        info( "\n***Initiate the FILLING PROCESS:\n" )

        s1.cmd('screen -dmS tank -L -Logfile ./logs/dt_screen_logs/tank-screen.log python physical_process.py')
        s1.cmd('screen -dmS bottle -L -Logfile ./logs/dt_screen_logs/bottle-screen.log python physical_process_bottle.py')
        plc3.cmd('screen -dmS plc3_process -L -Logfile ./logs/dt_screen_logs/plc3_process-screen.log bash plc3_loop.sh')
        plc2.cmd('screen -dmS plc2_process -L -Logfile ./logs/dt_screen_logs/plc2_process-screen.log bash plc2_loop.sh')
        plc1.cmd('screen -dmS plc1_process -L -Logfile ./logs/dt_screen_logs/plc1_process-screen.log bash plc1_loop.sh')
        
        
        # the DEFENSE CAPABILITY
        info( "\n***Initiate the DEFENSE CAPABILITY:\n" )
        
        ## run HIDS on PLC1 to log ICMP messages, ARP messages and log warning of ARP spoofing
        plc1.cmd('screen -dmS plc1_ids -L -Logfile ./logs/dt_screen_logs/plc1_ids-screen.log python hids.py plc1')
        plc2.cmd('screen -dmS plc2_ids -L -Logfile ./logs/dt_screen_logs/plc2_ids-screen.log python hids.py plc2')
        plc3.cmd('screen -dmS plc3_ids -L -Logfile ./logs/dt_screen_logs/plc3_ids-screen.log python hids.py plc3')
        
        ## run NIDS on HMI to perform ARP scan
        hmi.cmd('screen -dmS hmi_ids -L -Logfile ./logs/dt_screen_logs/hmi_ids-screen.log python nids_hmi.py')
        
        
        
        # the ATTACK CAPABILITY 
        info( "\n***Initiate the ATTACK CAPABILITY:\n" )
        
        ## run DoS attack via ICMP flooding
        #attacker.cmd('screen -dmS attacker_dos_attack -L -Logfile ./logs/dt_screen_logs/attacker_dos_attack-screen.log bash ./attack/dos_attack_a.sh')
                
        ## run MitM attack via ARP spoofing
        #attacker.cmd('screen -dmS attacker_mitm_attack -L -Logfile ./logs/dt_screen_logs/attacker_mitm_attack-screen.log bash ./attack/mitm_attack.sh')

        
        # additional screens for testing purposes 
        plc3.cmd('screen -dmS plc3_dump -L -Logfile ./logs/dt_screen_logs/plc3_dump-screen.log')
        plc2.cmd('screen -dmS plc2_dump -L -Logfile ./logs/dt_screen_logs/plc2_dump-screen.log')
        plc1.cmd('screen -dmS plc1_dump -L -Logfile ./logs/dt_screen_logs/plc1_dump-screen.log ')
        hmi.cmd('screen -dmS hmi_dump -L -Logfile ./logs/dt_screen_logs/hmi_dump-screen.log')
        attacker.cmd('screen -dmS attacker_dump -L -Logfile ./logs/dt_screen_logs/attacker_dump-screen.log')
        
        plc3.cmd('screen -dmS plc3 -L -Logfile ./logs/dt_screen_logs/plc3-screen.log')
        plc2.cmd('screen -dmS plc2 -L -Logfile ./logs/dt_screen_logs/plc2-screen.log')
        plc1.cmd('screen -dmS plc1 -L -Logfile ./logs/dt_screen_logs/plc1-screen.log')
        hmi.cmd('screen -dmS hmi -L -Logfile ./logs/dt_screen_logs/hmi-screen.log')
        attacker.cmd('screen -dmS attacker -L -Logfile ./logs/dt_screen_logs/attacker.log')
        attacker.cmd('screen -dmS attacker_mitm -L -Logfile ./logs/dt_screen_logs/attacker_mitm-screen.log')
        attacker.cmd('screen -dmS attacker_dos -L -Logfile ./logs/dt_screen_logs/attacker_dos-screen.log')
        

        # see the scripts running
        # NB: xterm required
        # uncomment the following lines (while removing the .cmd lines above)
        #net.terms += makeTerm(s1, display=None, cmd='python physical_process.py')
        #time.sleep(0.2)
        #net.terms += makeTerm(s1, display=None, cmd='python physical_process_bottle.py')
        #time.sleep(0.2)
        #net.terms += makeTerm(plc3, display=None, cmd='python plc3.py')    # display=None
        #time.sleep(0.2)
        #net.terms += makeTerm(plc2, display=None, cmd='python plc2.py')
        #time.sleep(0.2)
        #net.terms += makeTerm(plc1, display=None, cmd='python plc1.py')
 

        CLI(self.net)
        # self.net.stop()
        

if __name__ == "__main__":

    topo = FPTopo()
    net = Mininet(topo=topo)

    fpcps = FPCPS(
        name='FPCPS',
        net=net)

