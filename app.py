from flask import Flask, jsonify
from pymongo import MongoClient
import datetime
import re

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["test_db"]
    return db

@app.route('/')
def ping_server():
    return "Welcome!"

@app.route('/start')
def get_stored():
    db = get_db()
    _customers = db.test_db.find()
    customers = [{"id": customer["id"], "username": customer["username"], "password": customer["password"], "email": customer["email"] } for customer in _customers]
    return jsonify({"customers": customers})

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)