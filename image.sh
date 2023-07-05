#!/bin/bash
imageName=dharapat-prime-bank-cib:prod_v1.0

echo [LOG] Building docker image...
docker build --network=host -t $imageName -f DockerFile  .

echo [LOG] Tagging and pushing docker image to container registry...
docker tag $imageName dharapat.azurecr.io/$imageName
docker push dharapat.azurecr.io/$imageName