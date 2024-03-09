#!/bin/bash
imageName=dharapat-prime-bank-cib:uat_v3.1.0

echo [LOG] Building docker image...
docker buildx build --platform linux/x86_64 --network=host -t $imageName -f DockerFile  .

echo [LOG] Tagging and pushing docker image to container registry...
docker tag $imageName dharapat.azurecr.io/$imageName
docker push dharapat.azurecr.io/$imageName