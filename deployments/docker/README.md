# SIEM configuration

To connect Dsiem with the digital twin simulation, the following configuration files were adapted as described [here](https://github.com/defenxor/dsiem/blob/master/docs/event_processing.md).

Parse logs produced by the network hosts (e.g., PLC1, PLC2, etc) from the `src/logs` directory:

[filebeat.yml](./conf/filebeat/filebeat.yml)



Normalize logs to SIEM Events and create two indexes in Elasticsearch, one for events (`siem_events`) and one for alarms (`siem_alarms`):

[40_digitaltwin-pipeline.conf](./conf/logstash/conf.d/40_digitaltwin-pipeline.conf)

[70_dsiem-plugin_digital_twin.conf](./conf/logstash/conf.d/70_dsiem-plugin_digital_twin.conf)

[99_output.conf](./deployments/docker/conf/logstash/conf.d/99_output.conf)



 The correlation directives in JSON format are stored in the [configs](./conf/dsiem/configs) directory of Dsiem. 


# Editing the Kibana dashboard

The Kibana dashboard can easily be adpated to fit the current needs. To do so, open Kibana and edit, add or remove visualizations as necessary, then save the dashboard. 
To make the changes permanent, the dashboard config in the repo must be updated. Before proceeding, it is sensible to back up the current dashboard config. The config is stored at `DTCRforIR_backend/deployments/kibana/dashboard-siem.json`. 

To export the edited dashboard and save it, replace the host IP address of the cyber range VM in the following command and execuite it in the directory `DTCRforIR_backend/deployments/kibana`:

`curl -X GET http://199.999.9.99.166:5605/api/kibana/dashboards/export?dashboard=350e16e0-38b3-11ec-a547-a7b24e1b3b31 > dashboard-siem.json`