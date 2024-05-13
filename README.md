# docker-compose-flask-db-app

Docker-compose-flask-db-app is a Python app which run messaging site on flask.

## Requirements
Download requirements.txt and add secretsfile.py in your working directory
or any orther path in wich python can acsess this variables:
```bash
pip install -r requirements.txt
```

## Variables:
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
