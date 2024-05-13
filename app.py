
from flask import Flask, request,redirect,render_template
import requests
from random import sample,randint
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
    try:
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
                    return render_template('premessaging.html', msg = 'This login is used',recieved_message = senders_texts,your_login=sender)
                else:
                    dbf.update_row(dbname,table_name,'id',hash_id,column_name="login",text_value=text,ip=host,user=user,password=password)
                    return redirect('/pre_messaging/messaging')
            else:
                return render_template('premessaging.html')
    except:
        return redirect('/')


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
    try:    
        ip_addr = request.remote_addr
        hash_ip = sha256(str(ip_addr).encode()).hexdigest() #hashed ip
        sender = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)[0][3] #your login 
        value_find = dbf.find_in_table(dbname,"messaging",column_name="reciever",search_value=sender,ip=host,user=user,password=password) 
        value_find_sender = dbf.find_in_table(dbname,"messaging",column_name="sender",search_value=sender,ip=host,user=user,password=password)
        senders_texts = ' '
        recieved_texts = ' '
        #check messages sended to different users
        if value_find_sender is None:
            senders_texts += " "
        else: 
            for i in value_find_sender:
                sender_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[1]),ip=host,user=user,password=password)[0][0]
                reciever_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[2]),ip=host,user=user,password=password)[0][0]
                senders_texts += ' Sended message: '+ decryption(str(sender_hash+reciever_hash),i[3]).decode('utf-8') +" to " + str(i[2]) +";"

        #check messages recived from different users
        if value_find_sender is None:
            recieved_texts += " "
        else: 
            for i in value_find:
                sender_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[1]),ip=host,user=user,password=password)[0][0]
                reciever_hash = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(i[2]),ip=host,user=user,password=password)[0][0]
                recieved_texts += " "+ str(i[1]) + ' to you message:  '+ decryption(str(sender_hash+reciever_hash),i[3]).decode('utf-8') + ";"
        

        #who is ready to talk 
        Ready_talk=''
        for i in (dbf.find_column_in_table(dbname,table_name,column_name="login",ip=host,user=user,password=password) or''):
            if i[0] is not None:
                Ready_talk+= ' '+str(i[0])
        if sender is None:
            return redirect('/pre_messaging/')
        else:
        # send message from you to another user
            if request.method == 'POST' and 'message' in request.form and 'reciever' in request.form :
                    message = request.form['message']
                    reciever = request.form['reciever']
                    number_of_messages = (dbf.find_in_table(dbname,"messaging",column_name="reciever",search_value=reciever,ip=host,user=user,password=password) or '')
                    
                    #max number of messages to you from different users
                    if len(number_of_messages) >= 2:
                        return render_template('messaging.html',msg = "Max number of messages to reciever",your_login=sender,ready_talkers=Ready_talk)
                    
                    else:
                        #max len of the message,wich you can send
                        if len(message) >= 100:
                            return render_template('messaging.html', msg = 'Message is too long',ready_talkers=Ready_talk)

                        #print(dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password))
                        value_find_in_table = dbf.find_in_table(dbname,table_name,column_name="login",search_value=str(reciever),ip=host,user=user,password=password)
                        #if we found that reciever exists than
                        if len(value_find_in_table or '')>=1:
                            lens_of_messages =sha256((str(randint(0,1000)+randint(0,1000))).encode()).hexdigest()
                            secret1 = dbf.find_in_table(dbname,table_name,column_name="login",search_value=reciever,ip=host,user=user,password=password)[0][0]
                            secret2 = dbf.find_in_table(dbname,table_name,column_name="login",search_value=sender,ip=host,user=user,password=password)[0][0]
                            send_message = encryption(str(secret2+secret1),message)
                            dbf.insert_in_table(dbname,'messaging',columns_names="id",values=lens_of_messages,ip=host,user=user,password=password)
                            dbf.update_row(dbname,'messaging','id',lens_of_messages,column_name="sender",text_value=sender,ip=host,user=user,password=password)
                            dbf.update_row(dbname,'messaging','id',lens_of_messages,column_name="reciever",text_value=reciever,ip=host,user=user,password=password)
                            dbf.update_row(dbname,'messaging','id',lens_of_messages,column_name="message",text_value=str(send_message),ip=host,user=user,password=password)
                            sended_message = ' Sended message: ' +str(message)+ ' to '+ str(reciever)
                            return render_template('messaging.html', msg = 'Sended message ',recieved_messages= recieved_texts, your_login=sender, sended_messages= sended_message)
                        else:
                            
                            return render_template('messaging.html',msg = "message field is empty or reciever doesnt exist",recieved_messages= recieved_texts, your_login=sender, sended_messages= senders_texts,ready_talkers=Ready_talk)
            else: 
                return render_template('messaging.html',msg = "hi on messaging", recieved_messages=recieved_texts, your_login=sender, sended_messages= senders_texts,ready_talkers=Ready_talk)
    except IndexError:
        return redirect('/')


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
    try:
        ip_addr = request.remote_addr
        hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
        login = dbf.find_in_table(dbname,table_name,column_name="id",search_value=hash_id,ip=host,user=user,password=password)[0][3] 
        dbf.delete_row_in_table(dbname,table_name,column_name="id",search_value=str(hash_id),ip=host,user=user,password=password)
        dbf.delete_row_in_table(dbname,"messaging",column_name="sender",search_value=str(login),ip=host,user=user,password=password)
        return render_template('start.html')
    except IndexError:
        return render_template('start.html')


#def messaging


@app.route('/main_page', methods =['GET', 'POST'])
def main_page():
    try:
        ip_addr = request.remote_addr
        hash_id = sha256((str(ip_addr)+str(value_int)).encode()).hexdigest()
        dbf.find_in_table(dbname,table_name,column_name="id",search_value=str(hash_id),ip=host,user=user,password=password)[0][0] #check is user exsists in db
        text = "You can send message to administration"
        TOKEN = secretsfile.TOKEN
        chat_id = secretsfile.chat_id
        value_ip = dbf.find_in_table(dbname,table_name,column_name="ip",search_value=str(ip_addr),ip=host,user=user,password=password)
        # sends the message to admin chat in telegram
        if len(value_ip or '')>=1:
            value = "Your ip address: "+ str(ip_addr)
            if request.method == 'POST' and 'text' in request.form  :
                text = request.form['text']
                message = "from hash_id: "+ str(hash_id) + "  message: " + str(text)
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                requests.get(url).json() # sends the message to admin chat in telegram
                dbf.update_row(dbname,table_name,'id',hash_id,column_name="text",text_value=text,ip=host,user=user,password=password)
                text = "Message to administration: "+ str(text)
                return render_template('main.html', msg = text,value=value)
            else:
                return render_template('main.html', msg = text, value=value)
        else:
            return render_template('main.html', msg = text)
    except:
        return redirect('/')


@app.route('/')
def start_page():
    ip_addr = request.remote_addr
    global value_int
    hash_ip = sha256(str(ip_addr).encode()).hexdigest()
    value = dbf.find_in_table(dbname,table_name,column_name="hash_ip",search_value=str(hash_ip),ip=host,user=user,password=password)
    #print(value)
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