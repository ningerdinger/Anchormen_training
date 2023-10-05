# Docker Lab part 1

## Install Docker

Docker needs to be installed. Follow the guide:

* For Windows: https://docs.docker.com/docker-for-windows/install/
* For Mac: https://docs.docker.com/docker-for-mac/install/
* For Ubuntu: https://docs.docker.com/install/linux/docker-ce/ubuntu/ and follow these instructions:

  1. Add your user to the docker group.
  ```
  sudo usermod -aG docker $USER
  ```

  2. Log out and log back in so that your group membership is re-evaluated.

## Create a Dockerhub account

Create an account at https://hub.docker.com/
Export it:

```
export DOCKER_USER=YOUR_USER_NAME
```


## Create a Dockerfile

Create a Docker image of a simple Python web application.
You need to create a Dockerfile in order to build your image. A full reference to the Dockerfile format can be found here:

https://docs.docker.com/engine/reference/builder/

Some pointers:

* Use a base image containing Python from DockerHub - use the search function on https://hub.docker.com/
* You will need to copy the requirements.txt and app.py into the image
* You will need to expose the application port (5000)

Save the Dockerfile next to the app.py and requirements.txt

## Build your Docker image

```
docker build -t ${DOCKER_USER}/app .
```

## Run your Docker image to test

You will need to map the exposed port to a port on the host system.

```
docker run -p 5000:5000 ${DOCKER_USER}/app
```

The console should print a URL which you can open in your browser. Check to see if it works.

## Push your image to Docker Hub

First, you need to log in.

```
docker login
```

This will request your username and password.

Afterwards, you should be able to push your image:

```
docker push ${DOCKER_USER}/app
```

To see the locally available images just run:

```
docker image ls
```

To see all containers that are running run:

```
docker container ls
```

Since no containers are running (containers just terminate after they are done unless we tell them to keep running) we can also list all containers that ran by running:

```
docker container ls -a
```

We will be running multiple containers and leaving stray containers will eat up disk space. To remove containers we can run:

```
docker rm f67e310b0723
```

where f67e310b0723 is a Container ID listed in the docker container ls -a command. 

If we want to remove all exited docker containers in a single command just run:

```
docker container prune
```





