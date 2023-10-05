# Prometheus Lab

## Install Prometheus via helm 

Fetch the chart with the following command:

```
cd  ~/Documents # Or any other folder
mkdir prometheus
cd prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm fetch --untar prometheus-community/kube-prometheus-stack
```

and install as follows:

```
kubectl create namespace monitoring
helm install prometheus --namespace=monitoring kube-prometheus-stack
```

See more details about the kube-prometheus-stack [here](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) 

After some minutes, check that all pods are running in the namespace monitoring with the following command:

```
kubectl get pods -n monitoring
```

The Prometheus web admin interface now needs to be exposed to the Internet so that you can browse to it. To do so, create a new NodePort based Service, and expose the web admin interface on port **30900**. In the terminal execute the following commands:

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: prometheus-main
  namespace: monitoring
spec:
  type: NodePort
  ports:
  - port: 9090
    nodePort: 30900
  selector:
    prometheus: prometheus-kube-prometheus-prometheus
EOF
```

The Prometheus alert admin interface now needs to be exposed to the Internet so that you can browse to it. To do so, create a new NodePort based Service, and expose the web admin interface on port **30910**. In the terminal execute the following commands:

```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: prometheus-alert
  namespace: monitoring
spec:
  type: NodePort
  ports:
  - port: 9093
    nodePort: 30910
  selector:
     alertmanager: prometheus-kube-prometheus-alertmanager
EOF
```

Grafana admin interface now needs to be exposed to the Internet so that you can browse to it. To do so, create a new NodePort based Service, and expose the web admin interface on port **30920**. In the terminal execute the following commands:

```
kubectl expose deployment prometheus-grafana --type=NodePort --name=prometheus-grafana-ext --port=30920 --target-port=3000 -n monitoring
```

# Access Prometheus UI, Alerts and Grafana

Prometheus has its own UI which can be accessed by running the following command:

```
minikube service prometheus-main -n monitoring
```

if it doesn't open the UI automatically, then go to http://<MINIKUBE_IP>:30900

To get the MINIKUBE_IP, run:

```
minikube ip
```

Similarly, run the following command to access the Alert manager:

```
minikube service prometheus-alert -n monitoring
```

if it doesn't open the UI automatically, then go to http://<MINIKUBE_IP>:30910

To access Grafana, run the following command:

``` 
minikube service prometheus-grafana-ext -n monitoring
```

if it doesn't open the UI automatically, then go to http://<MINIKUBE_IP>:30920

To log in use these:

- username: admin
- password: prom-operator

# Grafana 
Grafana should be already linked with Prometheus. 
To check a dashboard, go to Dashboards (check icons in the left side) > manage.
Select Kubernetes / Compute Resources / Cluster. Values of your minikube cluster should appear.

- Import dashboard from grafana website 
    1. Go to https://grafana.com/grafana/dashboards
    2. Search for Kubernetes nodes 
    3. Sort by last updated since Prometheus has been recently updated.
    4. Pick one and copy the id. 
    5. Import the dashboard by going to Dashboards > Manage > Import
    6. Add the id to Grafana.com Dashboard, for example, 13493 or 5219. Press load
    7. Select Prometheus as prometheus target and click Import
    
- Import dashboard from json file 
    1. Go to Dashboards > Manage > Import
    2. Press Upload. json file and select all-nodes_rev1.json file (id 3131 from Grafana.com). 
    3. Press load
    4. Select Prometheus as prometheus target and click Import

Some of the panels are not updated. This is known problem which was generated after node_exporter renamed several metric names in v0.16. 
See [here](https://github.com/kubernetes-monitoring/kubernetes-mixin/issues/66) more details.

- Edit dashboard 
    1. Go to the dashboard to be edited (the one described below will be used as example).
    2. Press the name of a panel and select edit. 
    3. In the query panel, change node_cpu to node_cpu_seconds_total as indicated [here](https://github.com/kubernetes-monitoring/kubernetes-mixin/issues/66)
    4. Save the dashboard using the icon in the top left corner.

Change all the panels or import the Kubernetes All Nodes.json file as indicated below.



## Querying Prometheus

Open the prometheus UI as indicated below or just go [here](http://127.0.0.1:9090)

- Instant vector selectors with filtering
```
rest_client_requests_total{namespace="default"}
```

- Instant vector selectors with filtering by regex
```
rest_client_requests_total{namespace=~"def.*"}
```

- Operators
```
((sum(node_memory_MemTotal_bytes) - sum(node_memory_MemFree_bytes) - sum(node_memory_Buffers_bytes) - sum(node_memory_Cached_bytes)) / sum(node_memory_MemTotal_bytes)) * 100
```

- Functions with range vector selectors
```
rate(rest_client_requests_total[5m])
```

- Aggregation operators

```
rate(rest_client_requests_total{endpoint="https"}[5m])
```

```
sum(rest_client_requests_total) without (endpoint)
```

```
sum(rest_client_requests_total) by (endpoint)
```

Go [here](https://prometheus.io/docs/prometheus/latest/querying/basics/) for a detailed explanation 

## Preserve rules in Prometheus

Open the values.yaml file of the Prometheus installation and search for additionalPrometheusRulesMap: {}

Replace it with the following: 

```
additionalPrometheusRulesMap:
#  rule-name:
#    groups:
#    - name: my_group
#      rules:
#      - record: my_record
#        expr: 100 * my_record
 rule-name:
   groups:
   - name: httpvshttps
     rules:
     - record: endpoint:rest_client_requests_total:sum
       expr: sum(rest_client_requests_total) by (endpoint)
```
and run the following commands:

```
helm upgrade prometheus --namespace=monitoring kube-prometheus-stack
helm history prometheus --namespace=monitoring
```

Query the Prometheus UI for endpoint:rest_client_requests_total:sum, be patient it might take some time.


## Alerts rules in Prometheus

Open the values.yaml file of the Prometheus installation and search for additionalPrometheusRulesMap:

Add the following:
```         
   # Alerts
   - name: httpvshttps_alert
     rules:
     - alert: HighHttpTrafic
       expr: endpoint:rest_client_requests_total:sum{endpoint="http-metrics"} > 10
       for: 1m
       labels:
         severity: page
       annotations:
         summary: High HTTP traffic
```

it should look like this (see values.yaml file included):

```
additionalPrometheusRulesMap:
#  rule-name:
#    groups:
#    - name: my_group
#      rules:
#      - record: my_record
#        expr: 100 * my_record
 rule-name:
   groups:
   - name: httpvshttps
     rules:
     - record: endpoint:rest_client_requests_total:sum
       expr: sum(rest_client_requests_total) by (endpoint)
   # Alerts
   - name: httpvshttps_alert
     rules:
     - alert: HighHttpTrafic
       expr: endpoint:rest_client_requests_total:sum{endpoint="http-metrics"} > 10
       for: 1m
       labels:
         severity: page
       annotations:
         summary: High HTTP traffic
```

and run the following commands:

```
helm upgrade prometheus --namespace=monitoring kube-prometheus-stack
helm history prometheus --namespace=monitoring
```

Check that the alert alertname="HighHttpTrafic" has been added in the Alert Tab and it is triggered.

Then, open the Alert Manager and check that it also was included.

## Add a new target

We will add an new target using a redis server with an exporter as an example from [here](https://github.com/oliver006/redis_exporter).
A service was added to the original k8s-redis-and-exporter-deployment.yaml file and saved as redis.yaml, which is included.
Copy the redis.yaml included in the material in the actual folder and run the following command:

```
kubectl create -f redis.yaml
```
and check with:
```
kubectl get pods -n redis
kubectl get svc -n redis
```

To add this new target, edit the values.yaml from Prometheus as before. 
Search for additionalScrapeConfigs: [] and replace it with the following:

```
    additionalScrapeConfigs:
    # - job_name: kube-etcd
    #   kubernetes_sd_configs:
    #     - role: node
    #   scheme: https
    #   tls_config:
    #     ca_file:   /etc/prometheus/secrets/etcd-client-cert/etcd-ca
    #     cert_file: /etc/prometheus/secrets/etcd-client-cert/etcd-client
    #     key_file:  /etc/prometheus/secrets/etcd-client-cert/etcd-client-key
    #   relabel_configs:
    #   - action: labelmap
    #     regex: __meta_kubernetes_node_label_(.+)
    #   - source_labels: [__address__]
    #     action: replace
    #     target_label: __address__
    #     regex: ([^:;]+):(\d+)
    #     replacement: ${1}:2379
    #   - source_labels: [__meta_kubernetes_node_name]
    #     action: keep
    #     regex: .*mst.*
    #   - source_labels: [__meta_kubernetes_node_name]
    #     action: replace
    #     target_label: node
    #     regex: (.*)
    #     replacement: ${1}
    #   metric_relabel_configs:
    #   - regex: (kubernetes_io_hostname|failure_domain_beta_kubernetes_io_region|beta_kubernetes_io_os|beta_kubernetes_io_arch|beta_kubernetes_io_instance_type|failure_domain_beta_kubernetes_io_zone)
    #     action: labeldrop
      - job_name: 'redis'
        static_configs:
        - targets: ['redis.redis.svc.cluster.local:9121','redis.redis.svc.cluster.local:9121']
```

it should look like the values.yaml file included. Then run:

```
helm upgrade prometheus --namespace=monitoring kube-prometheus-stack
```

and check with:
``` 
helm history prometheus --namespace=monitoring
```

Check that the new target in Status > Targets appears and query the Prometheus UI for redis_cpu_sys_seconds_total 

## Clean 

Run the following:

```
kubectl delete -f redis.yaml
helm uninstall prometheus --namespace=monitoring
kubectl delete namespace monitoring
```

## Exercise setup a basic python app with some metrics available to Prometheus
See [here](https://github.com/prometheus/client_python) the official guide

See [here](https://medium.com/@ikod/custom-exporter-with-prometheus-b1c23cb24e7a) a detailed example