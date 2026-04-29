FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY gradlew settings.gradle.kts build.gradle.kts ./
COPY gradle ./gradle
COPY services/circleguard-form-service/build.gradle.kts services/circleguard-form-service/build.gradle.kts
COPY services/circleguard-form-service/src services/circleguard-form-service/src/
RUN chmod +x gradlew && ./gradlew :services:circleguard-form-service:bootJar -x test

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/services/circleguard-form-service/build/libs/*.jar app.jar
EXPOSE 8086
ENTRYPOINT ["java", "-jar", "app.jar"]
