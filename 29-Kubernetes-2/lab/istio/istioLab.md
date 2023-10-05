# Istio Lab

## Install Istio 

1. Get Istio 1.10.0 from https://github.com/istio/istio/releases/download/1.10.0/istio-1.10.0-linux-arm64.tar.gz
2. Untar it with:
```
cd ~/Downloads
tar -xvf istio-1.10.0-linux-arm64.tar.gz -C ~
```
2. Get k8s cluster with Helm
3. Install Istio

```
cd ~/istio-1.10.0
kubectl create namespace istio-system
helm install istio-base manifests/charts/base -n istio-system
helm install istiod manifests/charts/istio-control/istio-discovery \
	-n istio-system
helm install istio-ingress manifests/charts/gateways/istio-ingress \
	-n istio-system \
	--set gateways.istio-ingressgateway.type=NodePort
```

4. Install prometheus and Kiali

```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/prometheus.yaml
helm install \
  -n istio-system \
  --set auth.strategy="anonymous" \
  --repo https://kiali.org/helm-charts \
  kiali-server \
  kiali-server
kubectl get pods --namespace istio-system
```

5. Label default namespace:

```
kubectl label namespace default istio-injection=enabled
```
6. Install app:
```
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
```
7. Install gateway:
```
kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
```

8. Get urls as environmental variables:
```
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export GATEWAY_URL=$(minikube ip)
echo http://$GATEWAY_URL:$INGRESS_PORT/productpage
```

Go to this URL, for example http://192.168.10.2:31380/productpage

9. Check the KIALI UI:

```
kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=kiali -o jsonpath='{.items[0].metadata.name}') 20001:20001 &
```
Go to http://localhost:20001/kiali/console 

10. BOOKINFO demo:

- Default destination rule, run the following command:
```
kubectl apply -f samples/bookinfo/networking/destination-rule-all.yaml
```

Traffic is balanced among v1, v2 and v3. Check it out by reloading the bookinfo page several times and go to Kiali. In the Graph menu, select the default namespace and Versioned app graph.

- Route all to v1 service: 
```
kubectl apply -f samples/bookinfo/networking/virtual-service-all-v1.yaml
```

- Route user to v2 service: 
```
kubectl apply -f samples/bookinfo/networking/virtual-service-reviews-test-v2.yaml
```

user: password -> jason:jason


13. Clean up
```
kubectl delete -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f samples/bookinfo/networking/bookinfo-gateway.yaml
kubectl delete -f samples/bookinfo/networking/destination-rule-all.yaml
kubectl delete -f samples/bookinfo/networking/virtual-service-all-v1.yaml
kubectl delete -f samples/bookinfo/networking/virtual-service-reviews-test-v2.yaml
kubectl label namespace default istio-injection-
helm delete istio-ingress -n istio-system
helm delete istiod -n istio-system
helm delete istio-base -n istio-system
kubectl delete namespace istio-system
```





