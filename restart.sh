sudo docker rm -f poem
sudo docker run -d --name poem --runtime=nvidia --network="host" shixing19910105/poem:1.0 /bin/bash -c 'cd /home/poem/sh/ && bash run_all_docker.sh'
