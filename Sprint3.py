from pymongo import MongoClient
from flask import Flask, request,redirect,render_template
import datetime
import re
app = Flask(__name__)
app.secret_key = "secretkey"
@app.route('/register', methods =['GET', 'POST'])
def register():
    ip_addr = request.remote_addr
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if get_database_collection().find_one({"username":username}):
            msg = 'Username already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            x = get_database_collection()
            x.update_one({"ip":ip_addr},{"$set": { "username": username, "password": password, "email": email, "registration": 'yes'} })
            msg = 'You have successfully registered !'
    msg = 'registration'
    return render_template('register.html', msg = msg)
@app.route('/')
def start_page():
    ip_addr = request.remote_addr
    time = datetime.datetime.now()
    if get_database_collection().find_one({"ip":ip_addr}):
        print(get_database_collection().find_one({"ip":ip_addr}))
        return redirect('/start')
    else:
        visitor = {"ip": ip_addr,"time": time,"registration": "no"}
        visitor_collection_visitor = get_database_collection().insert_one(visitor)
        visitor_collection_visitor.inserted_id
        return redirect('/register')
@app.route('/start')
def start():
    ip_addr = request.remote_addr
    return render_template('start.html', msg = ip_addr)

# @app.route('/')
# def client():
#     ip_addr = request.environ['REMOTE_ADDR']
#     return '<h1> Your IP address is:' + ip_addr


# @app.route('/')
# def proxy_client():
#     ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
#     return ip_addr
def get_database_collection():
    dbname = get_database()
    visitor_collection = dbname["visitors_col"]
    return visitor_collection
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://oleksandrzaichko:h6UEVK4LvXAg4Udi@cluster0.0ramhdt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['who_logged_list']
  
# This is added so that many files can reuse the function get_database()
def write_logged_user():
    dbname = get_database()
    visitor_collection = dbname["visitors_col"]
if __name__ == "__main__":   
   # write logged user 

   # Get the database

   app.run(debug=True,port=8888,host='0.0.0.0')