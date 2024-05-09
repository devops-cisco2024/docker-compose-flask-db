
from flask import Flask, request,redirect,render_template
from random import randint
import databasefunctions as dbf
from hashlib import sha256
app = Flask(__name__)
app.secret_key = "secretkey"
dbname = "visitors"
password="password1"
user="user1"
host="192.168.142.136"
table_name = "visitors_info"
port=3306
value_int = 1

#redirect on accept and not page
@app.route('/start', methods =['GET', 'POST'])
def start():
    return render_template('accept_not.html')

#if accept 
@app.route("/move_accept/", methods=['POST'])
def move_accept():
    ip_addr = request.remote_addr
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    dbf.update_row(dbname,table_name,hash_id,column_name="ip",text_value=str(ip_addr),ip=host,user=user,password=password)
    return render_template('register.html')

#if not
@app.route("/move_notaccept/", methods=['POST'])
def move_notaccept():
    #Moving forward code
    return render_template('register.html')


@app.route('/register', methods =['GET', 'POST'])
def register():
    ip_addr = request.remote_addr
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    if request.method == 'POST' and 'text' in request.form  :
        text = request.form['text']
        dbf.update_row(dbname,table_name,hash_id,column_name="text",text_value=text,ip=host,user=user,password=password)

    return render_template('register.html', msg = text)


@app.route('/')
def start_page():
    ip_addr = request.remote_addr
    global value_int
    hash_ip = sha256(str(ip_addr).encode()).hexdigest()
    value = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)
    print(value)
    if len(value or '')>=1:
        print(value)
        return redirect('/register')
    else:
        while True:
            hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
            value_find_in_table = dbf.find_in_table(dbname,table_name,column_name="id",search_value=str(hash_id),ip=host,user=user,password=password)
            if len(value_find_in_table or '')>=1:
                value_int+=1
            else:
                dbf.insert_in_table(dbname,table_name,columns_names="id",values=hash_id,ip=host,user=user,password=password)
                dbf.update_row(dbname,table_name,hash_id,column_name="hash_ip",text_value=hash_ip,ip=host,user=user,password=password)
                return redirect('/start')
    


# 
# 
# ip_addr = request.environ['REMOTE_ADDR']
# 


# 
# 
# ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
# 
if __name__ == "__main__":   
   # write logged user 

   
   dbf.create_table(dbname,table_name,ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="id",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="ip",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="text",value_type="varchar(80)",ip=host,user=user,password=password)
   app.run(debug=True,port=8888,host='0.0.0.0')