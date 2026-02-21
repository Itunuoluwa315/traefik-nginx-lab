traefik-nginx-lab
Containerized NGINX web server behind Traefik reverse proxy using Docker Compose with HTTPS termination, automatic service discovery, and service isolation.

Containerized NGINX Web Server Behind Traefik

> Containerized NGINX web server behind Traefik reverse proxy using Docker Compose — features HTTPS termination, automatic service discovery, and service isolation.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Traefik](https://img.shields.io/badge/Traefik-24A1C1?style=for-the-badge&logo=traefikproxy&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![HTTPS](https://img.shields.io/badge/HTTPS-TLS%20Enabled-green?style=for-the-badge)

📋 Overview

This project demonstrates a production-grade containerized web infrastructure built for the **CYS 411 Cybersecurity Engineering** course. It deploys an NGINX static web server behind a Traefik reverse proxy using Docker Compose, implementing secure routing, HTTPS termination, automatic service discovery, and container network isolation.

Architecture

CLIENT BROWSER
       │
       │  HTTP :80 / HTTPS :443
       ▼
  ┌─────────────────────────────────┐
  │         TRAEFIK v2.10          │
  │   - :80  → redirects to HTTPS  │
  │   - :443 → TLS termination     │
  │   - :8080 → dashboard          │
  └────────┬────────────┬──────────┘
           │            │
    Discovers        Routes traffic
    via Docker API   to NGINX
           │            │
  ┌────────▼──────┐  ┌──▼──────────────┐
  │ DOCKER PROXY  │  │   NGINX Alpine   │
  │ API v bridge  │  │   Port 80        │
  │ Port: 2375    │  │   Static Site    │
  └───────────────┘  └─────────────────┘

  All containers: nginx_proxy_network (172.20.0.0/16)
```

---

## ✅ Features

- **NGINX** serving a static HTML website
- **Traefik** reverse proxy with automatic Docker service discovery
- **HTTPS** via self-signed TLS certificate (OpenSSL)
- **HTTP → HTTPS** automatic redirect
- **Service isolation** — NGINX has no exposed ports, only reachable through Traefik
- **Security headers** — X-Frame-Options, X-XSS-Protection, X-Content-Type-Options
- **Read-only volume mounts** on all config files
- **Docker API proxy** for Traefik compatibility with Docker Desktop 4.57+

---

## 📁 Project Structure

```
nginx/
├── docker-compose.yml          # Main orchestration file
├── docker-proxy.conf           # Docker API version compatibility proxy
├── traefik/
│   ├── traefik.yml             # Traefik static configuration
│   └── certs/
│       ├── cert.pem            # TLS certificate
│       └── key.pem             # TLS private key
└── nginx/
    ├── nginx.conf              # NGINX server configuration
    └── html/
        └── index.html          # Static website
```

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Docker TCP endpoint enabled at `localhost:2375`
  - Docker Desktop → Settings → General → **Expose daemon on tcp://localhost:2375**

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cys411-traefik-nginx-lab.git
cd cys411-traefik-nginx-lab
```

### 2. Generate self-signed TLS certificate
```bash
docker run --rm -v "${PWD}/traefik/certs:/certs" alpine/openssl req \
  -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /certs/key.pem \
  -out /certs/cert.pem \
  -subj "/CN=localhost/O=CYS411Lab"
```

### 3. Start all containers
```bash
docker compose up -d
```

### 4. Verify containers are running
```bash
docker compose ps
```

---

## 🌐 Access Points

| Service | URL | Description |
|---|---|---|
| Static Website | https://localhost | NGINX static site (accept cert warning) |
| HTTP Redirect | http://localhost | Auto-redirects to HTTPS |
| Traefik Dashboard | http://localhost:8080 | Shows discovered services and routers |

---

## ⚙️ Configuration

### docker-compose.yml
Defines all services, the isolated bridge network (`172.20.0.0/16`), and Traefik labels on the NGINX container for automatic service discovery.

### traefik/traefik.yml
Configures Traefik entry points (`:80` and `:443`), the Docker provider connection via the API proxy, and TLS certificate paths.

### nginx/nginx.conf
Configures NGINX with security headers and static file serving. `server_tokens off` hides the NGINX version from potential attackers.

### docker-proxy.conf
Bridges the Docker API version mismatch between Traefik v2.10 (requests API v1.24) and Docker Desktop 4.57+ (minimum API v1.44) by rewriting request paths.

---

## 🔒 Security Implementation

| Layer | Feature | Implementation |
|---|---|---|
| Transport | TLS Encryption | Self-signed cert, 2048-bit RSA |
| Routing | HTTP Redirect | Traefik entryPoint redirection |
| Network | Service Isolation | NGINX has no published ports |
| Discovery | Opt-in only | `exposedByDefault: false` |
| Headers | XSS Protection | NGINX security headers |
| Config | Immutable | All volumes mounted `:ro` |

---

## 📈 Scaling

Scale NGINX horizontally with one command — Traefik automatically load-balances:

```bash
docker compose up --scale nginx=3 -d
```

---

## 🛑 Shutdown

```bash
docker compose down
```

---

## 📚 Course

**CYS 411 — Cybersecurity Engineering**  
Assignment: Design and configure a containerized NGINX web server behind Traefik using Docker Compose with secure routing, HTTPS termination, service isolation, and automatic service discovery.
