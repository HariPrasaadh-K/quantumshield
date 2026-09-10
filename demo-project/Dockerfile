FROM openjdk:17-slim

RUN apt-get update && apt-get install -y \
    openssl \
    ca-certificates \
    certbot \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app

EXPOSE 8080 8443
CMD ["java", "-jar", "app.jar"]
