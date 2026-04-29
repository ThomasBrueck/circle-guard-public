FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY gradlew settings.gradle.kts build.gradle.kts ./
COPY gradle ./gradle
COPY services/circleguard-gateway-service/build.gradle.kts services/circleguard-gateway-service/build.gradle.kts
COPY services/circleguard-gateway-service/src services/circleguard-gateway-service/src/
RUN chmod +x gradlew && ./gradlew :services:circleguard-gateway-service:bootJar -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/services/circleguard-gateway-service/build/libs/*.jar app.jar
EXPOSE 8087
ENTRYPOINT ["java", "-jar", "app.jar"]
