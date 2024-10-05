#!/bin/bash

# Step 1: Pull Nginx Docker image
echo "Pulling Nginx Docker image..."
docker pull nginx:latest
HOST_IP=$(hostname -I | cut -d' ' -f1)
SYSTEMGUARD_PORT=5001
# STATIC_FOLDER=/path/to/static/folder

# Step 2: Create main Nginx configuration (nginx.conf)
echo "Creating main Nginx configuration..."

cat > nginx.conf <<EOL
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    # Define a log format for access logs
    log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                   '\$status \$body_bytes_sent "\$http_referer" '
                   '"\$http_user_agent" "\$http_x_forwarded_for"';

    # Enable gzip compression
    gzip on;
    gzip_types text/plain application/json application/javascript text/css application/xml;
    gzip_min_length 256;
    gzip_vary on;

    # Include all server configurations
    include /etc/nginx/conf.d/*.conf;
}
EOL

# Step 3: Create server configuration for Flask app (default.conf)
echo "Creating server configuration..."

cat > default.conf <<EOL
server {
    listen 80;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubdomains" always;
    add_header Referrer-Policy "no-referrer";

    # Proxy to Flask app
    location / {
        proxy_pass http://$HOST_IP:$SYSTEMGUARD_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # Client timeout settings
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }

    # Serve static files directly
    # location /static/ {
    #     alias $STATIC_FOLDER;
    #     expires -1;  # Disable caching
    #     add_header Cache-Control "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0";
    # }

    # Error pages
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    # Access and error log configuration
    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Limit body size to prevent large requests from overwhelming the server
    client_max_body_size 10M;

    # Buffer settings to optimize performance
    client_body_buffer_size 128k;
    proxy_buffer_size 4k;
    proxy_buffers 16 16k;
    proxy_busy_buffers_size 64k;

    # Deny access to sensitive files
    location ~ /\.ht {
        deny all;
    }
}
EOL

# Step 4: Start Nginx container with reverse proxy to Flask app
echo "Starting Nginx container..."
docker run -d --name nginx_proxy \
    -p 80:80 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf \
    -v $(pwd)/default.conf:/etc/nginx/conf.d/default.conf \
    nginx:latest

echo "Nginx reverse proxy set up successfully!"
