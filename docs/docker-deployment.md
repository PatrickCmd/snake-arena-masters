# Docker Deployment Guide

## Overview

This guide explains how to deploy Snake Arena Masters using Docker Compose with:
- **Frontend**: React app served by Nginx
- **Backend**: FastAPI application
- **Database**: PostgreSQL 17

## Prerequisites

- Docker Engine 20.10+
- Docker Compose V2

Verify installation:
```bash
docker --version
docker compose version
```

## Quick Start

### 1. Clone and Setup

```bash
cd snake-arena-masters
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file:
```bash
# Database
POSTGRES_DB=snake_arena
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password-here

# Backend
SECRET_KEY=your-secret-key-min-32-characters-long
```

#### Generate Secure SECRET_KEY

Use one of these commands to generate a cryptographically secure SECRET_KEY:

**Option 1: OpenSSL (recommended)**
```bash
openssl rand -hex 32
```

**Option 2: Python**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Option 3: /dev/urandom**
```bash
head -c 32 /dev/urandom | base64
```

Copy the generated value and paste it as your `SECRET_KEY` in the `.env` file.

### 3. Build and Start

```bash
# Build images
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

### 4. Access Application

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Initialize Database

The database is automatically initialized and seeded on first run.

**Demo Credentials:**
- Email: `demo@snake.game`
- Password: `demo123`

## Docker Commands

### Service Management

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View logs
docker compose logs -f [service]

# View status
docker compose ps
```

### Database Operations

```bash
# Run migrations
docker compose exec backend alembic upgrade head

# Seed database
docker compose exec backend python docker-entrypoint.py

# Access PostgreSQL
docker compose exec postgres psql -U postgres -d snake_arena

# Backup database
docker compose exec postgres pg_dump -U postgres snake_arena > backup.sql

# Restore database
docker compose exec -T postgres psql -U postgres snake_arena < backup.sql
```

### Development

```bash
# Rebuild specific service
docker compose build backend
docker compose up -d backend

# View backend logs
docker compose logs -f backend

# Execute command in container
docker compose exec backend python -m pytest

# Shell access
docker compose exec backend sh
docker compose exec frontend sh
```

## Architecture

### Services

#### Frontend (Nginx)
- **Port**: 80
- **Image**: Multi-stage build (Node → Nginx)
- **Features**:
  - Gzip compression
  - Security headers
  - API proxy to backend
  - Static asset caching

#### Backend (FastAPI)
- **Port**: 8000
- **Image**: Multi-stage build with uv
- **Features**:
  - Auto-migration on startup
  - Health checks
  - Non-root user

#### Database (PostgreSQL 17)
- **Internal Port**: 5432 (used by backend)
- **External Port**: 5433 (access from host machine)
- **Volume**: `postgres_data`
- **Features**:
  - Persistent storage
  - Health checks
  - Alpine-based image

**Port Mapping:**
- `5433:5432` means:
  - External: Access from host using `localhost:5433`
  - Internal: Backend connects using `postgres:5432`

**External Access Example:**
```bash
# Connect from host machine
psql -h localhost -p 5433 -U postgres -d snake_arena

# Or using Docker exec
docker compose exec postgres psql -U postgres -d snake_arena
```

### Network

All services communicate via `snake-arena-network` bridge network.

### Volumes

- `postgres_data`: PostgreSQL data persistence

## Production Deployment

### Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Use strong `SECRET_KEY` (min 32 characters)
- [ ] Enable HTTPS (use reverse proxy like Traefik/Nginx)
- [ ] Set up firewall rules
- [ ] Regular database backups
- [ ] Monitor logs and metrics

### Environment Variables

**Required:**
- `POSTGRES_PASSWORD`: Database password
- `SECRET_KEY`: JWT signing key

**Optional:**
- `POSTGRES_DB`: Database name (default: snake_arena)
- `POSTGRES_USER`: Database user (default: postgres)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry (default: 30)

### HTTPS Setup

Use a reverse proxy (Nginx/Traefik) in front of the frontend service:

```yaml
# docker-compose.override.yml
services:
  frontend:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.snake-arena.rule=Host(`yourdomain.com`)"
      - "traefik.http.routers.snake-arena.tls.certresolver=letsencrypt"
```

## Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs

# Check service health
docker compose ps

# Rebuild from scratch
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

### Database connection errors

```bash
# Check PostgreSQL is running
docker compose exec postgres pg_isready

# Verify environment variables
docker compose config

# Check network connectivity
docker compose exec backend ping postgres
```

### Frontend can't reach backend

```bash
# Check Nginx configuration
docker compose exec frontend cat /etc/nginx/conf.d/default.conf

# Test backend directly
curl http://localhost:8000/

# Check network
docker network inspect snake-arena-masters_snake-arena-network
```

### Permission errors

```bash
# Fix volume permissions
docker compose down
docker volume rm snake-arena-masters_postgres_data
docker compose up -d
```

## Monitoring

### Health Checks

```bash
# Backend health
curl http://localhost:8000/

# Frontend health
curl http://localhost/

# Database health
docker compose exec postgres pg_isready
```

### Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend

# Last 100 lines
docker compose logs --tail=100 backend
```

## Cleanup

```bash
# Stop and remove containers
docker compose down

# Remove volumes (WARNING: deletes data)
docker compose down -v

# Remove images
docker compose down --rmi all

# Complete cleanup
docker compose down -v --rmi all
docker system prune -a
```

## Development vs Production

### Development
```bash
# Use local code with hot reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Production
```bash
# Use optimized builds
docker compose up -d
```

## Support

For issues or questions:
1. Check logs: `docker compose logs -f`
2. Verify configuration: `docker compose config`
3. Review this guide
4. Check GitHub issues
