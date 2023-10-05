# Exercise 1

Reminder: All commando needs to be run from the same directory as this file.

## Building image

FOLLOW DOCKER FLASK-DEMO

# Deploy in Kubernetes

## Action I: Use Dashboard
The easiest way to deploy an app is using build-in dashboard:

1. Enable addons
```
minikube addons enable dashboard
```
2. Open minikube dashboard
```
minikube dashboard
```

We can create apps from the dashboard. For our first `deployment`, we will use the following. Change angelsevillacamins with your docker hub user name.

1. Use the Create button to create a new App
2. Under the tab `Create from form` fill the following settings:
   * App name: `demok8s-1`
   * Container image: `angelsevillacamins/app`
   * Number of pods: `1`
   * Service: External, Port `5000`, Target port `5000` and Protocol `TCP`
   * Namespace: Create a new namespace -> `exercise1`
   * Press Deploy
3. What will be created under the hood? Check the dashboard under namespace `exercise1`.
4. Starting the app can take a few minutes. Wait till everything is up, especially the service.
   1. The service will not come up under **Minikube** since it can't set up an external endpoint IP-address. Open a new terminal and use the command (keep this terminal open):
        ```bash
        minikube service demok8s-1 -n exercise1
        ```
      It should open automatically or you can open your app by opening the URL field in your browser, for example `http://192.168.99.102:31898`.
5. When everything is up, use the following command to see which services are running.
    ```bash
    kubectl get services -o wide -A
    ```

### Scale up

Go to `Deployments` in the dashboard, press the three circle symbol at the right of demok8s-1-XXXXXX and select scale. Set up to 3 pods. This means we will run 3 times our application in 3 containers.

Under `Pods` you will see the 3 pods running. Try to delete one of the pods. Reload the page after a few seconds. Can you explain what happened?

### Cleaning

1. Go to Deployments and delete demok8s-1
2. Go to Services and delete demok8s-1
3. Go to Namespaces and delete exercise1

## Action II: CLI commands:

With docker each container runs in a global docker environment. Inside kubernetes you can group containers in a group, which called a `namespace`.

Check which namespaces are available by default:
```bash
kubectl get namespaces
```

The first step is to create a namespace for our app.
```
kubectl create namespace exercise1
```

Check if the namespace is created:

* Use command line interface
* Check inside the dashboard

### 1. Create Deployment

Let's create our demo deployment using `kubectl create deployment` command, change angelsevillacamins with your docker hub user name:

```
kubectl create deployment --image angelsevillacamins/app --namespace exercise1 demok8s-1
```

The deployment automatically creates a `Pod` and `Replica Set` but no `Service`.

You can find the pods created with `kubectl get pods -n exercise1` command.

and see the details of the pod with `kubectl describe pods/<pod-id> -n exercise1` (this is somewhat similar to `docker container inspect`)

The deployment exist of one pod because we didn't specify the number of pods. We can can create a port forwarding to this single pod with the following command. Look for the pod id and replace the `<pod-id>` in the following command:

```
kubectl port-forward <pod-id> 5123:5000 --namespace exercise1
```

In the browser we can use `localhost:5123` to see the result.

### 2. Create Service

Pods are mortal, this mean when a pod dies it's not coming back automatically. This means above port forwarding only works till the pod dies. To have a more stable environment we can use load balancer that makes the application available on a specifc endpoint URL. The load balancer divide the traffic over the endpoints. When one is down, it will forward to the other pods. On the background an new pod will start till the desired number of pods is online.

We can use the following expose command to set up the load balancer.

```
kubectl expose deployment demok8s-1 --type=LoadBalancer --name demok8s-1-service --namespace exercise1 --port 5000 --target-port 5000
```

### 3. Check the work

Find the URL of the endpoint. You can use the following command to see the details of the service:

```
kubectl describe service/demok8s-1-service --namespace exercise1
minikube service demok8s-1-service -n exercise1
```

It should open automatically or you can open your app by opening the URL field in your browser, for example `http://192.168.99.102:31898`.

With the following command we can update our application and scale up to 3 pods:

```
kubectl scale deployments/demok8s-1 --replicas=3 --namespace exercise1
```
Check that now 3 pods are running (use `kubectl get pods --namespace exercise1` command)

### 4. Clean up
Now, let's clean up our deployment, service and namespace:
```
kubectl delete deployments/demok8s-1 svc/demok8s-1-service -n exercise1
kubectl delete namespace exercise1
```

## Action III: Use yaml files

Recall [Three Management Approaches](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/):
- **Imperative commands:** `create`, `expose`, `scale`
- **Imperative objects:** `create -f file.yml`, `expose -f file.yml`
- **Declarative objects:** `apply -f file.yml` or `dir/`

Look at the files `k8s/00_namespace.yaml`, `k8s/01_deployment.yaml` and `k8s/02_service.yaml`. The files explain the structure of our deployment, service and pods. 
Executing these files result in the same application as the previous docker lab.

```
kubectl apply -f k8s/
```
See what was created:
```
kubectl get all -n exercise1
```
If you want you can check if the demo works in browser and inspect created resourses (`kubectl describe`)  
How many replicas (pods) are running?

The use of yaml makes it easy to rollout an application on different kubernetes clusters. Most importantly, it allows for automation.

### Scale it!
Try to change yaml to scale down to 1 replica.  
Re-apply as you've done, and don't forget to check the results, e.g.:
```
kubectl get pods -n <namespace>`
```

### To clean:
just this:
```
kubectl delete -f k8s/
```