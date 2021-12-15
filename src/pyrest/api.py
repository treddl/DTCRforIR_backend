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


@app.route('/submit/<submit_data>', methods = ['POST','GET'])
@cross_origin()
def submit(submit_data):
    if (request.method == 'POST'):
        f = open("trainee_data.txt", "a")
        f.write(submit_data)
        f.close()
    return submit_data # a multidict containing POST data


# stops the entire cyber range 
# NB: including the API!
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

@app.route('/pull_frontend',methods=['GET'])
@cross_origin()
def pull_frontend():
    result_success = subprocess.check_output("bash src/git_pull_frontend.sh", shell=True)
    return "pulled frontendend from git"

@app.route('/pull_backend',methods=['GET'])
@cross_origin()
def pull_backend():
    result_success = subprocess.check_output("bash src/git_pull_backend.sh", shell=True)
    return "pulled backend from git"

app.run(port=9090, host="0.0.0.0")
