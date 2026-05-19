# Desplegar PostgreSQL local en el namespace DEV
resource "helm_release" "postgres_dev" {
  name       = "postgres-dev"
  repository = "oci://registry-1.docker.io/bitnamicharts"
  chart      = "postgresql"
  namespace  = kubernetes_namespace.dev.metadata[0].name
  timeout    = 300 

  set {
    name  = "auth.postgresPassword"
    value = "supersecretpassword"
  }
  set {
    name  = "auth.database"
    value = "circleguard_auth"
  }
  set {
    name  = "primary.persistence.enabled"
    value = "false"
  }
}

# Desplegar Kafka local en el namespace DEV (Para la mensajería de notificaciones)
resource "helm_release" "kafka_dev" {
  name       = "kafka-dev"
  repository = "oci://registry-1.docker.io/bitnamicharts"
  chart      = "kafka"
  namespace  = kubernetes_namespace.dev.metadata[0].name
  version    = "29.3.2"
  timeout    = 300

  set {
    name  = "replicaCount"
    value = "1"
  }
  set {
    name  = "controller.persistence.enabled"
    value = "false"
  }
  set {
    name  = "broker.persistence.enabled"
    value = "false"
  }
  set {
    name  = "image.repository"
    value = "bitnamilegacy/kafka"
  }
}

# Desplegar Redis local en el namespace DEV (Para cache y manejo de estados temporales)
resource "helm_release" "redis_dev" {
  name       = "redis-dev"
  repository = "oci://registry-1.docker.io/bitnamicharts"
  chart      = "redis"
  namespace  = kubernetes_namespace.dev.metadata[0].name
  timeout    = 300

  set {
    name  = "architecture"
    value = "standalone"
  }
  set {
    name  = "auth.enabled"
    value = "false"
  }
  set {
    name  = "master.persistence.enabled"
    value = "false"
  }
}
