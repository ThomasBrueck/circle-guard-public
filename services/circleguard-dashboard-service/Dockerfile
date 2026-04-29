FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY gradlew settings.gradle.kts build.gradle.kts ./
COPY gradle ./gradle
COPY services/circleguard-dashboard-service/build.gradle.kts services/circleguard-dashboard-service/build.gradle.kts
COPY services/circleguard-dashboard-service/src services/circleguard-dashboard-service/src/
RUN chmod +x gradlew && ./gradlew :services:circleguard-dashboard-service:bootJar -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/services/circleguard-dashboard-service/build/libs/*.jar app.jar
EXPOSE 8084
ENTRYPOINT ["java", "-jar", "app.jar"]
