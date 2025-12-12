# Build Stage
FROM node:18-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build
# Production Stage
FROM nginx:1.29.3-alpine

# Update Alpine packages to fix security vulnerabilities
RUN apk update && \
    apk upgrade --no-cache && \
    apk add --no-cache busybox>=1.37.0-r20 libpng>=1.6.53-r0

# Copiar ficheiros do build para o NGINX
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuração customizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy script to generate config.js
RUN echo '#!/bin/sh' > /docker-entrypoint.d/40-generate-config.sh && \
    echo 'cat <<EOF > /usr/share/nginx/html/config.js' >> /docker-entrypoint.d/40-generate-config.sh && \
    echo 'window.APP_CONFIG = {' >> /docker-entrypoint.d/40-generate-config.sh && \
    echo '  API_URL: "${API_URL:-http://localhost:5005}"' >> /docker-entrypoint.d/40-generate-config.sh && \
    echo '};' >> /docker-entrypoint.d/40-generate-config.sh && \
    echo 'EOF' >> /docker-entrypoint.d/40-generate-config.sh && \
    chmod +x /docker-entrypoint.d/40-generate-config.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
