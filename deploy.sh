#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd ~/backend
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop epajak
docker rm epajak
docker rmi -f setyoramdhoni07/epajak-reklame:be
docker run -d --name backend -p 5000:5000 setyoramdhoni07/epajak-reklame:be