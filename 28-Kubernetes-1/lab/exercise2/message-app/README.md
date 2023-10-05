# Docker Lab part 2

In this exercise we will create a simple REST API with two back end services. The application strives to follow the [twelve factor app
principles](https://12factor.net). We well configure and run the services as docker containers and by doing so we will cover a lot of the basic Docker command
line tools and how to work with Docker containers in general - it might be a good idea to have the [Docker CLI
reference](https://docs.docker.com/edge/engine/reference/commandline/docker/) open for this Lab.

## Running a First Container and Inspecting the Docker Environment

Before we start with our application let's check whether our environment is set up and functioning. Issue the following command to run a simple test container:

```
docker run hello-world
```

If all goes well your terminal should display output similar to the following:

```
 ~ → docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
d1725b59e92d: Pull complete
Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:

```
docker run -it ubuntu bash
```

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/


What just happened here is that Docker fetched the latest hello-world image from Docker Hub and started the downloaded container. While running a test 
container is a good way to inspect whether your docker environment is functioning there are other commands that can give you much more information on Docker.

Running: 

```
docker info
```

should give you an overview of the Docker configuration, system information, running containers and the like. 

## Initial Run of the API

With a functioning Docker environment we can start to set up our application. For this exercise we will set up a simple REST API leveraging
[Node.js](https://nodejs.org/en/) and [Sails](https://sailsjs.com). The HTTP Rest API exposes CRUD verbs on a *message* model. 

HTTP verb | URI | Action
----------| --- | ------
GET | /message | list all messages
GET | /message/ID | get message with ID
POST | /message | create a new message
PUT | /message/ID | modify message with ID
DELETE | /message/ID | delete message with ID


## Creating a Dockerfile

In this step we will use the sources to create our own Dockerfile. Edit the Dockerfile skeleton that is part of this repository and implement the steps
outlined. Please use the [Dockerfile reference](https://docs.docker.com/engine/reference/builder/) if you are uncertain which commands to use.

Once satisfied with your edits you can try to build the image by issuing a build command from the directory with the Dockerfile and message API sources:

```
docker build -t message-app:v0.2 .
```

Once the build is complete we can start all back end services:

1. Create a docker network for all our services so that they can reach each other: `docker network create messageapp`. Please take a moment to read the [Docker
   networking section](https://docs.docker.com/network/) of the documentation to get an idea of the possible network scenarios.
2. Start Redis in this network `docker run -d --name redis --net messageapp redis:alpine` - the `-d` option runs the container daemonized (in the background).
3. Start MongoDB in this network `docker run -d --name mongo --net messageapp mongo:3.2`

Finally start our API in the same network and set the environment 

```
docker run \
  -e MONGO_URL=mongodb://mongo/messageApp \
  -e REDIS_HOST=redis \
  -e PORT=80 \
  -p 8000:80 \
  --net messageapp \
   message-app:v0.2
```

Using a second shell try to use the API:

```
curl -XPOST http://localhost:8000/message?text=hello
```

And list the messages:

```
curl -XGET http://localhost:8000/message
[
  {
    "text": "hello",
    "createdAt": 1545335523264,
    "updatedAt": 1545335523264,
    "id": 1
  }
]
```

Play around some more with the API; create and delete some messages.

## Push your image to Docker Hub

First, you need to log in.

```
docker login
```

This will request your username and password.

Afterwards, you should be able to push your image:

```
docker push ${DOCKER_USER}/message-app:v0.2
```