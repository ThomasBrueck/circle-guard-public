import os

services = {
    'circleguard-gateway-service': 8087,
    'circleguard-auth-service': 8180,
    'circleguard-identity-service': 8083,
    'circleguard-form-service': 8086,
    'circleguard-notification-service': 8082,
    'circleguard-dashboard-service': 8084
}

base_dir = '/home/tbrueck/Documents/Semestre VIII/ingesoftV/taller-3/circle-guard-public'

# 1. Create Dockerfiles
for svc, port in services.items():
    dockerfile_path = os.path.join(base_dir, 'services', svc, 'Dockerfile')
    with open(dockerfile_path, 'w') as f:
        f.write(f"""FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY build.gradle.kts settings.gradle.kts gradlew ./
COPY gradle ./gradle
COPY src ./src
# Fallback to general gradle build if wrapper doesn't work correctly
RUN ./gradlew build -x test || gradle build -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar
EXPOSE {port}
ENTRYPOINT ["java", "-jar", "app.jar"]
""")

# 2. Create k8s/dev manifests
k8s_dev_dir = os.path.join(base_dir, 'k8s', 'dev')
os.makedirs(k8s_dev_dir, exist_ok=True)

for svc, port in services.items():
    k8s_path = os.path.join(k8s_dev_dir, f'{svc}-deployment.yaml')
    with open(k8s_path, 'w') as f:
        f.write(f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {svc}
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {svc}
  template:
    metadata:
      labels:
        app: {svc}
    spec:
      containers:
      - name: {svc}
        image: circle-guard/{svc}:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: {port}
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "dev"
---
apiVersion: v1
kind: Service
metadata:
  name: {svc}
  namespace: dev
spec:
  selector:
    app: {svc}
  ports:
  - port: 80
    targetPort: {port}
""")

# 3. Create pipelines
pipelines_dir = os.path.join(base_dir, 'pipelines')
os.makedirs(pipelines_dir, exist_ok=True)

for svc in services:
    jenkinsfile_path = os.path.join(pipelines_dir, f'Jenkinsfile.dev.{svc}')
    with open(jenkinsfile_path, 'w') as f:
        f.write(f"""pipeline {{
    agent any
    environment {{
        SERVICE_NAME = "{svc}"
        IMAGE_NAME   = "circle-guard/{svc}"
        IMAGE_TAG    = "${{env.BUILD_NUMBER}}"
        K8S_NS       = "dev"
    }}
    stages {{
        stage('Checkout') {{
            steps {{ checkout scm }}
        }}
        stage('Build Docker Image') {{
            steps {{
                dir("services/${{SERVICE_NAME}}") {{
                    sh "docker build -t ${{IMAGE_NAME}}:${{IMAGE_TAG}} ."
                    # Tag as latest for Minikube cache access
                    sh "docker tag ${{IMAGE_NAME}}:${{IMAGE_TAG}} ${{IMAGE_NAME}}:latest"
                }}
            }}
        }}
        stage('Unit Tests') {{
            steps {{
                dir("services/${{SERVICE_NAME}}") {{
                    sh "docker run --rm -v ${{WORKSPACE}}/services/${{SERVICE_NAME}}:/app -w /app eclipse-temurin:21-jdk-alpine ./gradlew test"
                }}
            }}
            post {{
                always {{
                    junit "services/${{SERVICE_NAME}}/build/test-results/**/*.xml"
                }}
            }}
        }}
        stage('Deploy to Dev K8s') {{
            steps {{
                sh "kubectl create namespace ${{K8S_NS}} --dry-run=client -o yaml | kubectl apply -f -"
                sh "kubectl apply -f k8s/dev/${{SERVICE_NAME}}-deployment.yaml -n ${{K8S_NS}}"
                sh "kubectl set image deployment/${{SERVICE_NAME}} ${{SERVICE_NAME}}=${{IMAGE_NAME}}:${{IMAGE_TAG}} -n ${{K8S_NS}}"
                sh "kubectl rollout status deployment/${{SERVICE_NAME}} -n ${{K8S_NS}} --timeout=120s"
            }}
        }}
    }}
    post {{
        failure {{
            echo "Pipeline FALLÓ para ${{SERVICE_NAME}}"
        }}
        success {{
            echo "Pipeline DEV completado para ${{SERVICE_NAME}}"
        }}
    }}
}}
""")

print("Dev files generated successfully.")
