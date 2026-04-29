#!/bin/bash
set -e

echo "=== Levantando infraestructura (DBs, Kafka, Redis, LDAP) ==="
docker compose -f docker-compose.dev.yml up -d

echo "=== Levantando Jenkins ==="
docker compose -f docker-compose.jenkins.yml up -d

echo "=== Iniciando Minikube ==="
# Intentamos iniciar minikube
./bin/minikube start --cpus=4 --memory=8192 || echo "Asegúrate de tener minikube instalado"

echo "=== Verificando nodos de Kubernetes ==="
./bin/kubectl get nodes || echo "Asegúrate de tener kubectl instalado"

echo "=== Listo ==="
echo "Jenkins corre en http://localhost:8080"
