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

import time


class FPCPS(MiniCPS):

    """Main container used to run the simulation."""

    def __init__(self, name, net):

        self.name = name
        self.net = net

        net.start()
        net.pingAll()

        # start devices
        plc1, plc2, plc3, s1, attacker, hmi = self.net.get('plc1', 'plc2', 'plc3', 's1',  'attacker', 'hmi')

        
        # run the scripts for the FILLING PROCESS in the respecitve mininet hosts
        s1.cmd('screen -dmS tank -L -Logfile ./logs/dt_screen_logs/tank-screen.log python physical_process.py')
        s1.cmd('screen -dmS bottle -L -Logfile ./logs/dt_screen_logs/bottle-screen.log python physical_process_bottle.py')
        plc3.cmd('screen -dmS plc3_process -L -Logfile ./logs/dt_screen_logs/plc3_process-screen.log bash plc3_loop.sh')
        plc2.cmd('screen -dmS plc2_process -L -Logfile ./logs/dt_screen_logs/plc2_process-screen.log bash plc2_loop.sh')
        plc1.cmd('screen -dmS plc1_process -L -Logfile ./logs/dt_screen_logs/plc1_process-screen.log bash plc1_loop.sh')
        
        
        
        # run the scripts for the DEFENSE CAPABILITY in the respecitve mininet hosts
        ## run HIDS on PLC1 to log ICMP messages, ARP messages and log warning of ARP spoofing
        #plc1.cmd('screen -dmS plc1_ids -L -Logfile ./logs/dt_screen_logs/plc1_ids-screen.log python hids_plc1.py ')
        
        ## run NIDS on HMI to log unkown hosts in the network
        #hmi.cmd('screen -dmS hmi_ids -L -Logfile ./logs/dt_screen_logs/hmi_ids-screen.log python nids_hmi.py ')
        
        
        
        # run the scripts for the ATTACK CAPABILITY in the respective mininet hosts
        ## run DoS attack via ICMP flooding
        #attacker.cmd('screen -dmS attacker_dos_attack -L -Logfile ./logs/dt_screen_logs/attacker_dos_attack-screen.log bash ./attack/dos_attack.sh')
        
        ## run MitM attack via ARP spoofing
        #attacker.cmd('screen -dmS attacker_mitm_attack -L -Logfile ./logs/dt_screen_logs/attacker_mitm_attack-screen.log bash ./attack/mitm_attack.sh')
        
        # create screens to get inside the nodes/hosts during run time
        s1.cmd('screen -dmSL s1_shell')
        plc3.cmd('screen -dmSL plc3_shell')
        plc2.cmd('screen -dmSL plc2_shell')
        plc1.cmd('screen -dmSL plc1_shell')
        hmi.cmd('screen -dmSL hmi_shell')
        attacker.cmd('screen -dmSL attacker_shell')
        

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
