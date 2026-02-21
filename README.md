# CYS 411 — Containerized NGINX Web Server Behind Traefik

Containerized NGINX web server behind Traefik reverse proxy using Docker Compose — features HTTPS termination, automatic service discovery, and service isolation.

---

## Overview

This project demonstrates a containerized web infrastructure built for the CYS 411 Cybersecurity Engineering course. It deploys an NGINX static web server behind a Traefik reverse proxy using Docker Compose, implementing secure routing, HTTPS termination, automatic service discovery, and container network isolation.

---

## Architecture

```
  CLIENT BROWSER
       |
       |  HTTP :80 / HTTPS :443
       |
  +-----------------------------+
  |       TRAEFIK v2.10         |
  |  :80  -> redirects HTTPS   |
  |  :443 -> TLS termination   |
  |  :8080 -> dashboard        |
  +--------+------------+-------+
           |            |
   Discovers via     Routes traffic
   Docker API        to NGINX
           |            |
  +--------+------+  +--+--------------+
  | DOCKER PROXY  |  | NGINX (Alpine)  |
  | API bridge    |  | Port: 80        |
  | Port: 2375    |  | Serves website  |
  +---------------+  +-----------------+

  Network: nginx_proxy_network (172.20.0.0/16)
```

---

## Features

- NGINX serving a static HTML website
- Traefik reverse proxy with automatic Docker service discovery
- HTTPS via self-signed TLS certificate
- HTTP to HTTPS automatic redirect
- Service isolation — NGINX has no exposed ports, only reachable through Traefik
- Security headers — X-Frame-Options, X-XSS-Protection, X-Content-Type-Options
- Read-only volume mounts on all configuration files
- Docker API proxy for Traefik compatibility with Docker Desktop 4.57+

---

## Project Structure

```
nginx/
├── docker-compose.yml
├── docker-proxy.conf
├── traefik/
│   ├── traefik.yml
│   └── certs/
│       ├── cert.pem
│       └── key.pem
└── nginx/
    ├── nginx.conf
    └── html/
        └── index.html
```

---

## Prerequisites

- Docker Desktop installed and running
- Docker TCP endpoint enabled at localhost:2375
  - Open Docker Desktop -> Settings -> General
  - Enable "Expose daemon on tcp://localhost:2375 without TLS"
  - Click Apply and Restart

---

## Setup and Deployment

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/cys411-traefik-nginx-lab.git
cd cys411-traefik-nginx-lab
```

### Step 2 — Generate the self-signed TLS certificate

```bash
docker run --rm -v "${PWD}/traefik/certs:/certs" alpine/openssl req \
  -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /certs/key.pem \
  -out /certs/cert.pem \
  -subj "/CN=localhost/O=CYS411Lab"
```

### Step 3 — Start all containers

```bash
docker compose up -d
```

### Step 4 — Verify everything is running

```bash
docker compose ps
docker compose logs traefik
```

---

## Access Points

| Service           | URL                   | Notes                                 |
|-------------------|-----------------------|---------------------------------------|
| Static Website    | https://localhost     | Accept the certificate warning        |
| HTTP Redirect     | http://localhost      | Automatically redirects to HTTPS      |
| Traefik Dashboard | http://localhost:8080 | Shows discovered routers and services |

---

## Configuration Files

**docker-compose.yml** — Defines all services, the isolated bridge network, volume mounts, and Traefik labels on the NGINX container for automatic service discovery.

**traefik/traefik.yml** — Configures Traefik entry points on port 80 and 443, the Docker provider connection via the API proxy, and TLS certificate paths.

**nginx/nginx.conf** — Configures NGINX with security headers and static file serving. Server tokens are disabled to hide the NGINX version from potential attackers.

**docker-proxy.conf** — Bridges the API version gap between Traefik v2.10, which requests Docker API v1.24, and Docker Desktop 4.57 which requires a minimum of API v1.44.

---

## Security

| Layer     | Feature            | How It Works                                       |
|-----------|--------------------|----------------------------------------------------|
| Transport | TLS Encryption     | Self-signed certificate, 2048-bit RSA              |
| Routing   | HTTP Redirect      | Traefik forces all traffic to HTTPS                |
| Network   | Service Isolation  | NGINX has no published ports                       |
| Discovery | Opt-in routing     | exposedByDefault is set to false                   |
| Headers   | Browser protection | X-Frame-Options, X-XSS-Protection, nosniff         |
| Config    | Read-only mounts   | All volumes mounted with :ro flag                  |

---

## Scaling

Traefik automatically detects and load-balances across multiple NGINX instances. Scale with one command and no configuration changes are needed:

```bash
docker compose up --scale nginx=3 -d
```

---

## Shutdown

```bash
docker compose down
```

---

## Course

CYS 411 — Cybersecurity Engineering

Assignment: Design and configure a containerized NGINX web server behind Traefik using Docker Compose with secure routing, HTTPS termination, service isolation, and automatic service discovery.
