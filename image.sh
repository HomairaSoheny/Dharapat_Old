#!/bin/bash
imageName=dharapat-prime-bank-cib:prod_v1.7

echo [LOG] Building docker image...
docker build --network=host -t $imageName -f DockerFile  .
docker docker buildx build --platform linux/amd64,linux/arm64 --network=host -t $imageName -f DockerFile  .

echo [LOG] Tagging and pushing docker image to container registry...
docker tag $imageName dharapat.azurecr.io/$imageName
docker push dharapat.azurecr.io/$imageName