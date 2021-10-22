"""
Provides the API.

Allows running commands inside the digital_twin container via the web browser

"""

import subprocess
import os
from subprocess import Popen, PIPE
from flask_cors import CORS, cross_origin
from subprocess import check_output
from flask import Flask
from flask import request


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/submit/<submit_data>', methods = ['POST','GET'])
@cross_origin()
def submit(submit_data):
    if (request.method == 'POST'):
        f = open("trainee_data.txt", "a")
        f.write(submit_data)
        f.close()
    return submit_data; # a multidict containing POST data

# stops the entire cyber range
@app.route('/stop_cr',methods=['GET'])
@cross_origin()
def compose():
    result_success = subprocess.check_output("bash stop.sh &>/dev/null", shell=True);
    return "successfully shut down cyber range infrastructure";

# restarts the entire cyber range
@app.route('/restart_cr',methods=['GET'])
@cross_origin()
def docker():
    result_success = subprocess.check_output("bash restart.sh &>/dev/null", shell=True)
    return "successfully started cyber range infrastructure";

# restarts the digital_twin container
@app.route('/restart_dt_container',methods=['GET'])
@cross_origin()
def restart():
    result_success = subprocess.check_output("bash restart_dt_container.sh", shell=True);
    return "restarted dt";

ip_vm = subprocess.check_output("bash get_ip.sh", shell=True).decode("utf-8").rstrip();
print(ip_vm)
#ip_vm=ipaddress.IPv4Address(ip_vm)

app.run(port=9090, host=ip_vm)