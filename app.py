
from flask import Flask, request,redirect,render_template
from random import randint
import databasefunctions as dbf
from hashlib import sha256,md5
import secretsfile
import base64
from cryptography.fernet import Fernet 
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
#to work with nginx 
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
app.secret_key = secretsfile.secret_key
dbname = secretsfile.dbname
password=secretsfile.password
user=secretsfile.user
host=secretsfile.host
table_name = secretsfile.table_name
port=secretsfile.port
value_int = 1
message_number = 1

def find_logins(dbname,table_name,column_name,ip,user,password):
    logins =  dbf.find_column_in_table(dbname,table_name,column_name,ip,user,password)
    value
    for i in logins:
        if logins is not None:
            value += logins
    return value


def encryption(string_key,text):
    key = gen_fernet_key(sha256((string_key).encode()).hexdigest().encode('utf-8'))
    f = Fernet(key)
    return f.encrypt(text.encode('ascii')).decode('utf-8')
def decryption(string_key,encoded_text):
    key = gen_fernet_key(sha256((string_key).encode()).hexdigest().encode('utf-8'))
    f = Fernet(key)
    return f.decrypt(encoded_text)


#creating key for securing our messagin text
def gen_fernet_key(passcode:bytes) -> bytes:
    assert isinstance(passcode, bytes)
    hlib = md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

@app.route('/pre_messaging/', methods =['GET', 'POST'])
def pre_messaging():
    ip_addr = request.remote_addr
    hash_ip = sha256(str(ip_addr).encode()).hexdigest()
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    name_in_table = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)
    sender = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)[0][3]
    value_find = (dbf.find_in_table_for_list(dbname,"messaging",column_name="reciever,id",search_value=(sender,message_number),ip=host,user=user,password=password) or'')
    senders_texts = 'From'

    for i in value_find:
        sender_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[1]),ip=host,user=user,password=password)[0][0]
        senders_texts += str(i[1]) + 'to'+ decryption(str(sender_hash+hash_id),i[3]).decode('utf-8')

     #check number of messages to you from different users
    if len(name_in_table or '')>=1 and name_in_table[0][3] is not None:
        return redirect('/pre_messaging/messaging')
    
    else:
        if request.method == 'POST' and 'text' in request.form  :
            text = request.form['text'].lower()
            value_find_in_table = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(text),ip=host,user=user,password=password)
            if len(value_find_in_table or '')>=1:

                return render_template('pre_messaging.html', msg = 'This login is used',recieved_message = senders_texts,your_login=sender)
            else:
                dbf.update_row(dbname,table_name,'id',hash_id,column_name="login",text_value=text,ip=host,user=user,password=password)
                return redirect('/pre_messaging/messaging')
        else:
            return render_template('premessaging.html')


@app.route("/pre_messaging/delete_message/", methods=['POST'])
def delete_message():
    ip_addr = request.remote_addr
    hash_ip = sha256(str(ip_addr).encode()).hexdigest() #hashed ip
    sender = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)[0][3] #your login 
    dbf.delete_row_in_table(dbname,'messaging',column_name="reciever",search_value=str(sender),ip=host,user=user,password=password)
    return redirect('/pre_messaging/messaging')
#messagin page


@app.route('/pre_messaging/messaging', methods =['GET', 'POST'])
def messaging():
    ip_addr = request.remote_addr
    hash_ip = sha256(str(ip_addr).encode()).hexdigest() #hashed ip
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest() #hashed id
    sender = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)[0][3] #your login 
    value_find = (dbf.find_in_table_for_list(dbname,"messaging",column_name="reciever,id",search_value=(sender,message_number),ip=host,user=user,password=password) or'') 
    senders_texts = 'From '
    #check number of messages to you from different users

    for i in value_find:
        sender_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[1]),ip=host,user=user,password=password)[0][0]
        senders_texts += str(i[1]) + ' to you '+ decryption(str(sender_hash+hash_id),i[3]).decode('utf-8')


    # send message from you to another user
    if request.method == 'POST' and 'message' in request.form and 'reciever' in request.form  :
            message = request.form['message']
            reciever = request.form['reciever']
            number_of_messages = (dbf.find_in_table(dbname,"messaging",column_name="reciever",search_value=reciever,ip=host,user=user,password=password) or '')
            
            #max number of messages to you from different users
            if len(number_of_messages) >= 1:
                return render_template('messaging.html',msg = "Max number of messages to reciever",your_login=sender)
            
            else:
                #max len of the message,wich you can send
                if len(message) >= 100:
                    return render_template('messaging.html', msg = 'Message is too long')

                print(dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password))
                value_find_in_table = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(reciever),ip=host,user=user,password=password)
                #if we found that reciever exists than
                if len(value_find_in_table or '')>=1:

                    secret1 = dbf.find_in_table(dbname,table_name,column_name="login",search_value=reciever,ip=host,user=user,password=password)[0][0]
                    secret2 = dbf.find_in_table(dbname,table_name,column_name="login",search_value=sender,ip=host,user=user,password=password)[0][0]
                    send_message = encryption(str(secret1+secret2),message)
                    dbf.insert_in_table(dbname,'messaging',columns_names="id",values=message_number,ip=host,user=user,password=password)
                    dbf.update_row(dbname,'messaging','id',message_number,column_name="sender",text_value=sender,ip=host,user=user,password=password)
                    dbf.update_row(dbname,'messaging','id',message_number,column_name="reciever",text_value=reciever,ip=host,user=user,password=password)
                    dbf.update_row(dbname,'messaging','id',message_number,column_name="message",text_value=str(send_message),ip=host,user=user,password=password)

                    return render_template('messaging.html', msg = 'This login is used')
                else:
                    
                    return render_template('messaging.html',msg = "message field is empty or reciever doesnt exist",recieved_messages= senders_texts,your_login=sender)
    else: 
        return render_template('messaging.html',msg = "hi on messaging",recieved_messages=senders_texts,your_login=sender )


#redirect on accept and not page
@app.route('/start', methods =['GET', 'POST'])
def start():

    return render_template('accept_not.html')

#if accept 
@app.route("/move_accept/", methods=['POST'])
def move_accept():

    ip_addr = request.remote_addr
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    dbf.update_row(dbname,table_name,'id',hash_id,column_name="ip",text_value=str(ip_addr),ip=host,user=user,password=password)

    return redirect('/main_page')

#if not
@app.route("/move_notaccept/", methods=['POST'])
def move_notaccept():
    #Moving forward code
    return redirect('/main_page')


#if our visitor whant to delete value from table
@app.route("/move_delete/", methods=['POST'])
def move_delete():
    ip_addr = request.remote_addr
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    dbf.delete_row_in_table(dbname,table_name,column_name="id",search_value=str(hash_id),ip=host,user=user,password=password)
    return render_template('start.html')


#def messaging


@app.route('/main_page', methods =['GET', 'POST'])
def main_page():
    ip_addr = request.remote_addr
    hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
    text = "you are here"
    value = ""
    value_ip = dbf.find_in_table(dbname,table_name,column_name="ip",search_value=str(ip_addr),ip=host,user=user,password=password)
    print(value)
    if len(value_ip or '')>=1:
        return render_template('main.html', msg = text,value=ip_addr)
    else:
        if request.method == 'POST' and 'text' in request.form  :
            text = request.form['text']
            dbf.update_row(dbname,table_name,'id',hash_id,column_name="text",text_value=text,ip=host,user=user,password=password)

        return render_template('main.html', msg = text)


@app.route('/')
def start_page():
    ip_addr = request.remote_addr
    global value_int
    hash_ip = sha256(str(ip_addr).encode()).hexdigest()
    value = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)
    print(value)
    if len(value or '')>=1:
        return redirect('/main_page')
    else:
        while True:
            hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
            value_find_in_table = dbf.find_in_table(dbname,table_name,column_name="id",search_value=str(hash_id),ip=host,user=user,password=password)
            if len(value_find_in_table or '')>=1:
                value_int+=1
            else:
                dbf.insert_in_table(dbname,table_name,columns_names="id",values=hash_id,ip=host,user=user,password=password)
                dbf.update_row(dbname,table_name,'id',hash_id,column_name="hash_ip",text_value=hash_ip,ip=host,user=user,password=password)
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


   dbf.create_table(dbname,table_name,ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="hash_ip",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="ip",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="login",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,table_name,column_name="text",value_type="varchar(80)",ip=host,user=user,password=password)




   dbf.create_table(dbname,'messaging',ip=host,user=user,password=password)
   dbf.add_column(dbname,'messaging',column_name="sender",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,'messaging',column_name="reciever",value_type="varchar(80)",ip=host,user=user,password=password)
   dbf.add_column(dbname,'messaging',column_name="message",value_type="varchar(2000)",ip=host,user=user,password=password)
   app.run(debug=True,port=8888,host='0.0.0.0')