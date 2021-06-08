# Simple Kafka example

This implementation produces orders and prepares drinks.

![architecture](./docs/plantuml-arch.png)

Run the following commands to get started:

```bash
foo@host:~$ git clone https://github.com/hughpearse/kafka-example
foo@host:~$ cd kafka-example
```

## Docker

```bash
foo@host:~$ docker stop $(docker ps -a -q)
foo@host:~$ docker rm $(docker ps -a -q)
foo@host:~$ docker-compose build
foo@host:~$ docker-compose up
foo@host:~$ curl -X POST -H "Content-Type: application/json" http://localhost:8080/order -d '{"name":"coconut"}'
foo@host:~$ curl -X GET -H "Accept: application/json" http://localhost:8080/collect
```

## Kubernetes (made with kompose)

```bash
foo@bar$ minikube stop
foo@bar$ minikube delete --all
foo@bar$ rm -rf ~/.kube
foo@bar$ minikube start
foo@bar$ eval $(minikube docker-env)
foo@bar$ docker-compose build
foo@bar$ cd k8s
foo@bar$ kubectl apply -f bartender.yaml,kafka.yaml,waiter.yaml,zookeeper.yaml
foo@bar$ minikube tunnel --cleanup
foo@bar$ minikube ssh 'sudo ip link set docker0 promisc on'
foo@bar$ curl -X POST -H "Content-Type: application/json" http://localhost:8080/order -d '{"name":"coconut"}'
foo@bar$ curl -X GET -H "Accept: application/json" http://127.0.0.1:8080/collect
foo@bar$ kubectl delete -f bartender.yaml,kafka.yaml,waiter.yaml,zookeeper.yaml
foo@bar$ minikube stop
```

made using:

```bash
foo@bar$ kompose convert
```

## Kubernetes with Istio

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
foo@bar$ curl -X GET -H "Accept: application/json" -HHost:istio.default.waiter.com 127.0.0.1:80/collect
foo@bar$ killall istioctl
```

## Openshift

```bash
foo@bar$ minishift start --network-nameserver 8.8.8.8
foo@bar$ eval $(minishift oc-env)
foo@bar$ oc login -u system:admin -n default
foo@bar$ oc new-project demo
foo@bar$ oc adm policy add-role-to-user system:registry developer
foo@bar$ oc adm policy add-role-to-user system:image-builder developer
foo@bar$ oc adm policy add-role-to-user admin developer -n demo
foo@bar$ oc login -u developer
foo@bar$ eval $(minishift docker-env)
foo@bar$ export DREG=$(minishift openshift registry)
foo@bar$ docker login -u $(oc whoami) -p $(oc whoami -t) $(minishift openshift registry)
foo@bar$ docker build ./waiter -t ${DREG}/demo/waiter:1.0
foo@bar$ docker build ./bartender -t ${DREG}/demo/bartender:1.0
foo@bar$ docker push ${DREG}/demo/waiter:1.0
foo@bar$ docker push ${DREG}/demo/bartender:1.0
foo@bar$ docker-compose pull kafka zookeeper
foo@bar$ docker tag bitnami/kafka:2.8.0 ${DREG}/demo/kafka:2.8.0
foo@bar$ docker tag bitnami/zookeeper:3.7.0 ${DREG}/demo/zookeeper:3.7.0
foo@bar$ docker push ${DREG}/demo/kafka:2.8.0
foo@bar$ docker push ${DREG}/demo/zookeeper:3.7.0
foo@bar$ oc apply -f ./openshift/
foo@bar$ oc expose service waiter -n demo
foo@bar$ minishift ssh 'sudo ip link set docker0 promisc on'
foo@bar$ oc get route -o=jsonpath="{range .items[*]}{.spec.host}{'\n'}"
foo@bar$ curl -X POST -H "Content-Type: application/json" waiter-demo.192.168.64.16.nip.io/order -d '{"name":"coconut"}'
foo@bar$ curl waiter-demo.192.168.64.9.nip.io/collect
foo@bar$ minishift console # developer / developer
```

Test using

```bash
foo@bar$ oc scale --replicas=1 dc waiter
foo@bar$ oc get all
foo@bar$ siege -c255 -t10S 'waiter-demo.192.168.64.28.nip.io/order POST {"name":"coconut"}' --content-type 'application/json'
foo@bar$ oc scale --replicas=10 dc waiter
foo@bar$ oc get all
foo@bar$ siege -c255 -t10S 'waiter-demo.192.168.64.28.nip.io/order POST {"name":"coconut"}' --content-type 'application/json'
```

made using:

```bash
foo@bar$ kompose convert --provider=openshift
```
