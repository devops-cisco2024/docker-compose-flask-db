#!/bin/bash
# Script for synchronizing backups to Google Cloud Storage

# Path to the backup folder
backup_path="./backup"

# The name of your bucket in GCS
bucket_name="backup_flask_app"

# File synchronization
gsutil -m rsync -r ${backup_path} gs://${bucket_name}/

