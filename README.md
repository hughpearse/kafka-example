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

Alternatuveely run in kubernetes

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
```
