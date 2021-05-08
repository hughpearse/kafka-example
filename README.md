# Simple Kafka example

This implementation produces orders and prepares drinks.

Run the following commands:

```bash
foo@host:~$ docker stop $(docker ps -a -q)
foo@host:~$ docker rm $(docker ps -a -q)
foo@host:~$ docker-compose build
foo@host:~$ docker-compose up
foo@host:~$ curl -X POST -H "Content-Type: application/json" http://localhost:8080/order -d '{"name":"coconut"}'
foo@host:~$ curl -X GET -H "Accept: application/json" http://localhost:8080/collect
```

![architecture](./docs/plantuml-arch.png)

Alternatively run in kubernetes

```bash
foo@bar$ minikube start
foo@bar$ eval $(minikube docker-env)
foo@bar$ docker-compose build
foo@bar$ cd k8s
foo@bar$ kubectl delete all --all
foo@bar$ kubectl apply -f bartender.yaml,kafka.yaml,waiter.yaml,zookeeper.yaml
foo@bar$ minikube tunnel --cleanup
foo@bar$ minikube ssh 'sudo ip link set docker0 promisc on'
foo@bar$ curl -X POST -H "Content-Type: application/json" http://localhost:8080/order -d '{"name":"coconut"}'
foo@bar$ curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/collect
foo@bar$ kubectl delete -f bartender.yaml,kafka.yaml,waiter.yaml,zookeeper.yaml
foo@bar$ minikube stop
```

Run with Istio

```bash
foo@bar$ brew install istioctl
foo@bar$ minikube start
foo@bar$ istioctl install
foo@bar$ kubectl label namespace default istio-injection=enabled
foo@bar$ kubectl get ns default --show-labels
foo@bar$ cd k8s
foo@bar$ kubectl apply -f bartender.yaml,kafka.yaml,waiter.yaml,zookeeper.yaml
foo@bar$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.9/samples/addons/kiali.yaml
foo@bar$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.9/samples/addons/prometheus.yaml
foo@bar$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.9/samples/addons/grafana.yaml
foo@bar$ kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.9/samples/addons/jaeger.yaml
foo@bar$ kubectl get svc -n istio-system
foo@bar$ istioctl dashboard jaeger &
foo@bar$ istioctl dashboard grafana &
foo@bar$ istioctl dashboard prometheus &
foo@bar$ istioctl dashboard kiali &
foo@bar$ cd ./../istio/
foo@bar$ kubectl apply -f ./istio-ingress-gateway.yaml
foo@bar$ minikube tunnel --cleanup
foo@bar$ curl -X POST -H "Content-Type: application/json" -HHost:istio.default.waiter.com http://127.0.0.1:80/order -d '{"name":"coconut"}'
foo@bar$ curl -HHost:istio.default.waiter.com 127.0.0.1:80/collect
foo@bar$ killall istioctl
```

Alternatively run in openshift

```bash
foo@bar$ minikube stop
foo@bar$ minishift stop
foo@bar$ minishift delete --force --clear-cache
foo@bar$ minikube delete --all
foo@bar$ rm -rf ~/.minishift
foo@bar$ rm -rf ~/.kube
foo@bar$ sudo chown root:wheel /usr/local/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
foo@bar$ sudo chmod u+s /usr/local/opt/docker-machine-driver-xhyve/bin/docker-machine-driver-xhyve
foo@bar$ sudo chmod u+s /usr/local/bin/hyperkit
foo@bar$ minishift start
foo@bar$ oc myapp .
foo@bar$ TODO
foo@bar$
foo@bar$
foo@bar$
foo@bar$
foo@bar$
```
