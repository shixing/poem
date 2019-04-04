sudo docker rm -f poem
sudo docker run -d --name poem --runtime=nvidia -p 4000:4000 -p 8080:8080 shixing19910105/poem:1.0 /bin/bash -c 'cd /home/poem/sh/ && bash run_all_docker.sh'
