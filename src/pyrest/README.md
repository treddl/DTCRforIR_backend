# API

The REST-API is implemented with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and connects the different components of the cyber range (i.e., the virtual environent, the SIEM system, and the LMS).

## Purpose & Function

The API has two main purposes. First, to provide a management layer for the trainer. Second, to faciliate the flow of the exercise. 

It thus basically serves as a way to change the cyber range's system state. To change the system state, a predefined keyword bound to the cyber range's host IP address and the port number the API is listening on is called. 

### Management 

The API provides functionalities for the trainer to manage the cyber range training in the following ways:

- `199.999.9.99:9090/cr_stop` to stop and reset the microservice infrastructure and the frontend of the cyber range 
- `199.999.9.99:9090/cr_start` to restart the microservice infrastructure and the frontend
- `199.999.9.99:9090/restart_dt` to restart the digital twin simulation

### Exercise progression 

The actions of the trainees are bound to API calls which run a sanitized version of the commands provided and actions performed by the trainee. This is to minimize unexpected errors that could be thrown during a cyber range exercise. Ultimately, this ensures that all trainees have the same learning experience.

- `199.999.9.99:9090/start_mitm`
- `199.999.9.99:9090/stop_mitm`
- `199.999.9.99:9090/start_dos_a`
- `199.999.9.99:9090/start_dos_b`
- `199.999.9.99:9090/start_dos_c`
- `199.999.9.99:9090/stop_dos`
- `199.999.9.99:9090/arp_scan`