# Exercise 2 - Message App

Reminder: All commando need to be run from the same directory as this file.

## Deploy to kubernetes

Try to deploy the app in kubernetes.  
The recommeded way is to create one or multiple yamls which you can run with `kubectl apply -f k8s/file.yml` or simply `kubectl apply -f k8s/`.  
The following steps can serve you as guidance in the proccess:
- Create yamls for the following components:
  
   1. Namespace exercise2
   2. Redis deployment exposing port 6379 (with image redis:alpine)
   3. Redis service exposing port 6379.
   4. MongoDB deployment exposing port 27017 (with image mongo:3.4)
   5. MongoDB service exposing port 27017.
   6. messageapp deployment exposing port 80 (with image angelsevillacamins/message-app:v0.2 or your own image).
   7. messageapp service as type LoadBalancer exposing port 80.
- Don't forget to add env variables MONGO_URL, REDIS_HOST and PORT to messageapp pod template (find out how to do it):
   - MONGO_URL="mongodb://mongo/messageApp"
   - REDIS_HOST="redis"
   - PORT="80"
- Look at the additional slides and example yaml in the `example` subfolder and   
  remeber to take care about:
   - `kind` and correct `apiVersion`
   - required parts in yaml
   - `labels` and `selector`
   - correct image name, tag
   - copy your yaml(s) to `/k8s` subfolder
- Don't hesitate to use `kubectl api-resources`, and `kubectl explain <resource>.<object>.<object>...` commands for help   
not least `kubectl get <resource>`, `describe`, `logs` for debuging
- Do check documentation to find out more nuances of:
   - Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment, https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service
   - Services: https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service
   - or kubernetes docs: https://kubernetes.io/docs/home/

## III. Finally, test your Deployment

```
kubectl apply -f k8s/
kubectl get pods -n exercise2
kubectl get services -n exercise2
```
and:

```
minikube service messageapp -n exercise2
```

then:

```
minikube service list
```

Copy url and port for NAMESPACE=exercise2 and NAME=messageapp service and run:

```
curl -XPOST http://192.168.99.100:30204/message?text=hello
```

Copy url and port for NAMESPACE=exercise2 and NAME=messageapp service and list the messages:

```
curl -XGET http://192.168.99.100:30204/message
[
  {
    "text": "hello",
    "createdAt": 1545335523264,
    "updatedAt": 1545335523264,
    "id": 1
  }
]
```

### To clean:
```
kubectl delete -f k8s/01_all.yaml
```

### Clean up minikube
```
minikube stop
minikube delete
```