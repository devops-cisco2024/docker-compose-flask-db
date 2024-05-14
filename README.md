
# docker-compose-flask-db-app

Docker-compose-flask-db-app is a Python app which run messaging site on flask.

## Requirements
Download requirements.txt and add secretsfile.py in your working directory
or any orther path in wich python can acsess this variables:
```bash
pip install -r requirements.txt
```

## Variables in secretsfile.py:
```python
#any value in string for secret key to sign session cookies
secret_key = "key"

#mariadb database name where stored information about users
dbname = "dbname"

#password which used to accsess to db by username
password="password"

#any username that can acsess to db
user="username"

#ip of database
host="ip"

#table where information about users will be stored
table_name = "table name"

#port which used to connect to the db
port=int(value)

#token of your telegram bot
TOKEN="string"

#chat id in which telegram bot will send messages from users to the administration
chat_id = "string"
```

Start the app.py with the command 
```bash
python3 app.py
```
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

# Backup

## Description
This section contains instructions for setting up database backups using Docker and Google Cloud Storage.

## Backup Setup

### Starting the Backup Service
To get started, run `docker-compose.yml` from the `backup` folder. The service will automatically create a database dump every hour and save it to the `backup` folder.

### Configuring Backups to Google Cloud Storage

#### Google Cloud Authentication
Authenticate to Google Cloud and configure your project with the following commands:
```sh
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```
Replace [YOUR_PROJECT_ID] with your Google Cloud project's ID.

Creating and Configuring a Service Account
Create a service account and grant it access to your Google Storage:

Create a service account in the Google Cloud Console.
Download the key in JSON format.
Set up environment variables to use this key:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-file.json"
```
Replace the path with the actual path to your service account key file.

Setting up Synchronization
Edit the sync_backups.sh file, specifying the name of your Google Storage bucket. Example line in the script:
```sh
gsutil cp /path/to/backup/* gs://your-google-storage-bucket
```

Replace /path/to/backup/* and your-google-storage-bucket with the actual values.

Configuring cron for Automatic Synchronization
Set up the cron service to run the sync_backups.sh script according to a schedule by adding the following line to your crontab:
```sh
0 * * * * /path/to/sync_backups.sh
```
# Monitoring

## Description
This section outlines the monitoring setup using Prometheus, Grafana, and various exporters to track the health and performance of both the server and the containers running the application and database.

## Monitoring Architecture

### Exporters
- **Cadvisor Exporter**: Gathers metrics from containers, helping monitor their performance and resource usage.
- **Node Exporter**: Collects metrics from the server itself, providing insights into system-level metrics.
- **Blackbox Exporter**: Monitors the uptime and SSL/TLS certificate status of websites.

### Setup Requirements
To run Prometheus and Grafana, you will need a separate server with Docker installed. This server will host these tools to avoid any performance overhead on your application server.

### Launching Monitoring Services
Navigate to the `monitoring` folder in the repository and run the following command to start Prometheus and Grafana using Docker Compose:
```sh
docker-compose up -d
```
Configuring Prometheus and Blackbox Exporter
Edit the prometheus.yml and blackbox-exporter-config.yml configuration files to match your specific monitoring requirements. This may include setting up scrape intervals, targets, and alert rules for Prometheus, as well as specific modules and probe settings for the Blackbox Exporter.


