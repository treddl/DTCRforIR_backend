# preparation to stop containers gracefully
cd ../../src
## reverses the dsiem directives from .json to .txt
bash deactivate_directives.sh
## quits all running screen sessions in the Docker container 'digital_twin'
sudo docker exec -it digital_twin bash quit_screen.sh
## quits the screen 'frontend' in the baselayer VM
screen -X -S frontend quit

# stop containers
cd ../deployments/docker
sudo docker-compose stop 
sudo docker container rm elasticsearch 
sudo docker volume rm docker_es-data 
