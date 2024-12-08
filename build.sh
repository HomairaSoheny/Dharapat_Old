#!/bin/bash
#imageName=dharapat-prime-bank-cib:uat_v3.1.30
imageName=dharapat-prime-bank-cib:dev_v3.1.31

echo [LOG] Building docker image...
docker buildx build --platform linux/x86_64 --network=host -t $imageName -f DockerFile  .

echo [LOG] Tagging and pushing docker image to container registry...
docker tag $imageName dharapat.azurecr.io/$imageName
docker push dharapat.azurecr.io/$imageName


docker buildx build --platform linux/x86_64 --network=host -t dharapat-prime-bank-cib:dev_v3.1.31 -f DockerFile  .
docker tag dharapat-prime-bank-cib:dev_v3.1.31 dharapat.azurecr.io/dharapat-prime-bank-cib:dev_v3.1.31
docker push dharapat.azurecr.io/dharapat-prime-bank-cib:dev_v3.1.31