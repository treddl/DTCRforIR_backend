"""
Provides the API.

Note: requires an IP address in dot-notation as first argument (e.g., python api.py 192.168.2.166)

Allows running commands inside the digital_twin container via the web browser

"""

import subprocess
import os
import sys
from subprocess import Popen, PIPE
from flask_cors import CORS, cross_origin
from subprocess import check_output
from flask import Flask
from flask import request


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['GET'])
@cross_origin()
def start_page():
    message = "This is the cyber range's API."
    return message

# starts the MitM attack via ARP spoofing
@app.route('/start_mitm',methods=['GET'])
@cross_origin()
def mitm_start():
    result_success = subprocess.check_output("bash src/mitm_attack_start.sh &>/dev/null", shell=True)
    message = 'sucessfully started the MitM attack via ARP spoofing'
    print(message)
    return message

# stops the MitM attack via ARP spoofing
@app.route('/stop_mitm',methods=['GET'])
@cross_origin()
def mitm_stop():
    result_success = subprocess.check_output("bash src/mitm_attack_stop.sh &>/dev/null", shell=True)
    message = 'sucessfully stopped the MitM attack via ARP spoofing'
    print(message)
    return message

# starts the DoS attack with attacker host as source IP address
@app.route('/start_dos_a',methods=['GET'])
@cross_origin()
def dos_start_a():
    result_success = subprocess.check_output("bash src/dos_attack_a.sh &>/dev/null", shell=True)
    message = 'sucessfully started the DoS attack via ICMP flooding with attacker host as source IP address'
    print(message)
    return message

# starts the DoS attack with attacker host as source IP address
@app.route('/start_dos_b',methods=['GET'])
@cross_origin()
def dos_start_b():
    result_success = subprocess.check_output("bash src/dos_attack_b.sh &>/dev/null", shell=True)
    message = 'sucessfully started the DoS attack via ICMP flooding with spoofed host as source IP address'
    print(message)
    return message

# starts the DoS attack with attacker host as source IP address
@app.route('/start_dos_c',methods=['GET'])
@cross_origin()
def dos_start_c():
    result_success = subprocess.check_output("bash src/dos_attack_c.sh &>/dev/null", shell=True)
    message = 'sucessfully started the (distributed) DoS attack via ICMP flooding with spoofed random hosts as source IP addresses'
    print(message)
    return message

# stop any of the DoS attacks
@app.route('/stop_dos',methods=['GET'])
@cross_origin()
def dos_stop():
    result_success = subprocess.check_output("bash src/dos_attack_stop.sh &>/dev/null", shell=True)
    message = 'sucessfully stopped the DoS attack via ICMP flooding'
    print(message)
    return message


# perform ARP scan from HMI
@app.route('/arp_scan',methods=['GET'])
@cross_origin()
def arp_scan():
    result_success = subprocess.check_output("bash src/arp_scan.sh &>/dev/null", shell=True)
    message = 'sucessfully ran ARP scan from the HMI'
    print(message)
    return message


@app.route('/submit/<submit_data>', methods = ['POST','GET'])
@cross_origin()
def submit(submit_data):
    if (request.method == 'POST'):
        f = open("trainee_data.txt", "a")
        f.write(submit_data)
        f.close()
    return submit_data # a multidict containing POST data


# stops the entire cyber range
@app.route('/stop_cr',methods=['GET'])
@cross_origin()
def compose():
    result_success = subprocess.check_output("bash src/stop.sh &>/dev/null", shell=True)
    return "successfully shut down cyber range infrastructure"

# restarts the entire cyber range
@app.route('/restart_cr',methods=['GET'])
@cross_origin()
def docker():
    result_success = subprocess.check_output("bash src/restart.sh &>/dev/null", shell=True)
    message = "successfully started cyber range infrastructure"
    print(message)
    return message

# restarts the digital_twin container
@app.route('/restart_dt_container',methods=['GET'])
@cross_origin()
def restart():
    result_success = subprocess.check_output("bash src/restart_dt_container.sh", shell=True)
    return "restarted dt"


ip_vm = sys.argv[1]
print('API is running on IP address:')
print(ip_vm)
#ip_vm=ipaddress.IPv4Address(ip_vm)

app.run(port=9090, host=ip_vm)