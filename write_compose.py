content = """networks:
  proxy_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1

services:

  traefik:
    image: traefik:v3.3
    container_name: traefik
    restart: unless-stopped
    user: "root"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - ./traefik/traefik.yml:/etc/traefik/traefik.yml:ro
      - ./traefik/certs:/certs:ro
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - proxy_network

  nginx:
    image: nginx:alpine
    container_name: nginx_web
    restart: unless-stopped
    volumes:
      - ./nginx/html:/usr/share/nginx/html:ro
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - proxy_network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`localhost`)"
      - "traefik.http.routers.nginx.entrypoints=websecure"
      - "traefik.http.routers.nginx.tls=true"
      - "traefik.http.services.nginx.loadbalancer.server.port=80"
"""

with open("docker-compose.yml", "w") as f:
    f.write(content)
print("Done! Check the file:")
with open("docker-compose.yml") as f:
    for line in f:
        if "localhost" in line:
            print(repr(line))