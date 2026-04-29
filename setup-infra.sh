#!/bin/bash
set -e

KUBECTL_VERSION="v1.29.0"
MINIKUBE_VERSION="v1.32.0"
ARCH="amd64"

mkdir -p bin

echo "=== Descargando herramientas si no existen ==="
if [ ! -f bin/kubectl ]; then
    echo "Descargando kubectl ${KUBECTL_VERSION}..."
    curl -Lo bin/kubectl "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${ARCH}/kubectl"
    chmod +x bin/kubectl
    echo "kubectl listo"
fi

if [ ! -f bin/minikube ]; then
    echo "Descargando minikube ${MINIKUBE_VERSION}..."
    curl -Lo bin/minikube "https://storage.googleapis.com/minikube/releases/${MINIKUBE_VERSION}/minikube-linux-${ARCH}"
    chmod +x bin/minikube
    echo "minikube listo"
fi

echo "=== Levantando infraestructura (DBs, Kafka, Redis, LDAP) ==="
docker compose -f docker-compose.dev.yml up -d

echo "=== Levantando Jenkins ==="
docker compose -f docker-compose.jenkins.yml up -d

echo "=== Iniciando Minikube ==="
./bin/minikube start --cpus=4 --memory=8192

echo "=== Verificando nodos de Kubernetes ==="
./bin/kubectl get nodes

echo "=== Listo ==="
echo "Jenkins corre en http://localhost:8080"
