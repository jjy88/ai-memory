# Deployment Guide

This guide covers various deployment options for the AI Memory application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Environment Variables](#environment-variables)
- [Monitoring & Logging](#monitoring--logging)

## Prerequisites

### Required
- Python 3.11+
- Redis 6.0+ (for caching and task queues)

### Optional
- Docker & Docker Compose
- Nginx (for production)
- PostgreSQL (for persistent storage - future)

## Local Development

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/jjy88/ai-memory.git
cd ai-memory

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

### 3. Start Redis (Optional)

```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install locally and run
redis-server
```

### 4. Run Application

```bash
# Direct run
python main.py

# Or using Make
make run
```

Visit `http://localhost:5000` to access the application.

## Docker Deployment

### Development with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services included:
- Web application (port 8000)
- Redis (port 6379)
- Celery worker
- Celery beat (scheduled tasks)

### Production Docker Build

```bash
# Build image
docker build -t ai-memory:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret \
  -e JWT_SECRET_KEY=your-jwt-secret \
  -e REDIS_URL=redis://redis:6379/0 \
  --name ai-memory \
  ai-memory:latest
```

## Production Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Install Redis
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Install Nginx
sudo apt install nginx
```

### 2. Application Setup

```bash
# Create app directory
sudo mkdir -p /var/www/ai-memory
sudo chown $USER:$USER /var/www/ai-memory
cd /var/www/ai-memory

# Clone repository
git clone https://github.com/jjy88/ai-memory.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Systemd Service

Create `/etc/systemd/system/ai-memory.service`:

```ini
[Unit]
Description=AI Memory Web Application
After=network.target redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-memory
Environment="PATH=/var/www/ai-memory/venv/bin"
EnvironmentFile=/var/www/ai-memory/.env
ExecStart=/var/www/ai-memory/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/ai-memory/access.log \
    --error-logfile /var/log/ai-memory/error.log \
    main:app

[Install]
WantedBy=multi-user.target
```

Create Celery worker service `/etc/systemd/system/ai-memory-worker.service`:

```ini
[Unit]
Description=AI Memory Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-memory
Environment="PATH=/var/www/ai-memory/venv/bin"
EnvironmentFile=/var/www/ai-memory/.env
ExecStart=/var/www/ai-memory/venv/bin/celery -A tasks.celery worker \
    --loglevel=info \
    --logfile=/var/log/ai-memory/celery-worker.log

[Install]
WantedBy=multi-user.target
```

Start services:

```bash
# Create log directory
sudo mkdir -p /var/log/ai-memory
sudo chown www-data:www-data /var/log/ai-memory

# Enable and start services
sudo systemctl enable ai-memory
sudo systemctl enable ai-memory-worker
sudo systemctl start ai-memory
sudo systemctl start ai-memory-worker

# Check status
sudo systemctl status ai-memory
sudo systemctl status ai-memory-worker
```

### 4. Configure Nginx

Create `/etc/nginx/sites-available/ai-memory`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL certificates (use certbot for Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Upload size limit
    client_max_body_size 150M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /var/www/ai-memory/static;
        expires 30d;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ai-memory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

## Cloud Platforms

### Heroku

1. Create `Procfile` (already included):
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 main:app
worker: celery -A tasks.celery worker --loglevel=info
```

2. Deploy:
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret

# Deploy
git push heroku main

# Scale workers
heroku ps:scale web=1 worker=1
```

### AWS (EC2)

1. Launch EC2 instance (Ubuntu 22.04)
2. Follow [Production Deployment](#production-deployment) steps
3. Configure security groups:
   - Allow HTTP (80)
   - Allow HTTPS (443)
   - Allow SSH (22) from your IP

### Google Cloud Platform (Cloud Run)

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-memory

# Deploy
gcloud run deploy ai-memory \
  --image gcr.io/PROJECT_ID/ai-memory \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SECRET_KEY=xxx,JWT_SECRET_KEY=xxx
```

## Environment Variables

### Required

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### Optional

```bash
# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Custom Domain
CUSTOM_DOMAIN=obsicat.com

# Port
PORT=8000
```

### Generating Secrets

```bash
# Generate random secret keys
python -c "import secrets; print(secrets.token_hex(32))"
```

## Monitoring & Logging

### Application Logs

```bash
# View systemd logs
sudo journalctl -u ai-memory -f

# View Celery logs
sudo journalctl -u ai-memory-worker -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check

```bash
# Check application health
curl http://localhost:8000/health

# Should return:
# {"status": "healthy", "version": "1.0.0"}
```

### Performance Monitoring

Consider adding:
- **Sentry** for error tracking
- **Prometheus + Grafana** for metrics
- **ELK Stack** for log aggregation
- **New Relic / DataDog** for APM

## Backup & Recovery

### Database Backup (when using PostgreSQL)

```bash
# Backup
pg_dump ai_memory > backup.sql

# Restore
psql ai_memory < backup.sql
```

### File Uploads

```bash
# Backup uploads directory
tar -czf uploads-backup.tar.gz uploads/

# Restore
tar -xzf uploads-backup.tar.gz
```

## Troubleshooting

### Common Issues

**Redis Connection Error**
```bash
# Check if Redis is running
sudo systemctl status redis-server

# Test Redis connection
redis-cli ping
```

**Permission Errors**
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/ai-memory
```

**Port Already in Use**
```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

## Security Checklist

- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS with SSL certificate
- [ ] Configure firewall (ufw/iptables)
- [ ] Keep dependencies updated
- [ ] Regular security audits
- [ ] Implement proper logging
- [ ] Set up monitoring and alerts
- [ ] Regular backups
- [ ] Limit file upload sizes
- [ ] Implement rate limiting

## Support

For issues or questions:
- [GitHub Issues](https://github.com/jjy88/ai-memory/issues)
- [Documentation](https://github.com/jjy88/ai-memory)
