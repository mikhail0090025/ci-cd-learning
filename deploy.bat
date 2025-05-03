@echo off
docker stop my-ml-container || exit /b 0
docker rm my-ml-container || exit /b 0
docker pull %DOCKER_HUB_USERNAME%/my-container:latest
docker run -d -v D:/TS TEMP:/app/data --name my-ml-container %DOCKER_HUB_USERNAME%/my-container:latest
echo Deployment complete!
pause