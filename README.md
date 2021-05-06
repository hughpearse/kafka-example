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
foo@bar$ docker image ls -a
foo@bar$ kompose convert
foo@bar$ kubectl apply -f bartender-deployment.yaml,kafka-deployment.yaml,kafka-service.yaml,waiter-deployment.yaml,waiter-service.yaml,zookeeper-deployment.yaml,zookeeper-service.yaml
foo@bar$ kubectl get po
foo@bar$ kubectl expose deployment waiter --name=myloadbalander --port=8080 --target-port=8080 --type=LoadBalancer
foo@bar$ minikube tunnel --cleanup
foo@bar$ kubectl get svc
foo@bar$ curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/collect
```
