# Docker-compose-flask-db application

Before starting the docker-compose.yaml file:
- you should create a named volume by command:
```bash
docker volume create db-data
```
- replace the variable values in the .env file with your own.
- change path to nginx SSL certificates in `nginx/default.conf` and `nginx/Dockerfile` files

Build application image with command:
```bash
docker compose build
```
Start the `docker-compose.yaml` file with the command (you can use the `-d` option for starting in detached mode):
```bash
docker compose up
```
