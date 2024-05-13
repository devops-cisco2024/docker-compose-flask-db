import mariadb
import sys

#implement starting connection point
def connection_to_db(ip,dbname,user,password):
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=ip,
            port=3306,
            database=dbname

        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)

#create table in aout db
def create_table(dbname,table_name,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to Mariadb")
        #cursor.execute("DROP TABLE IF EXISTS " +table_name)
        sql_update_query = """CREATE TABLE %s (
        id VARCHAR(80))"""
        cursor.execute(sql_update_query % (table_name))
        mariadbConnection.commit()
        #print("Table created successfully")
        cursor.close()

    except mariadb.Error as error:
        print("Failed to create table in mariadb", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")

#update value of a row
def update_row(dbname,table_name,search_id,hash_id,column_name,text_value,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")

        sql_update_query = """Update %s set %s = '%s' where %s = '%s'"""
        cursor.execute(sql_update_query % (table_name,column_name,text_value,search_id,hash_id))
        mariadbConnection.commit()
        #print("Record Updated successfully ")
        cursor.close()

    except mariadb.Error as error:
        print("Failed to update mariadb table", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")

#add column in a table 
def add_column(dbname,table_name,column_name,value_type,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")

        sql_update_query = """Alter table %s add %s %s"""
        cursor.execute(sql_update_query % (table_name,column_name,value_type))
        mariadbConnection.commit()
        #print("alter table successfully ")
        cursor.close()

    except mariadb.Error as error:
        print("Failed to alter mariadb table", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The ariadb connection is closed")

#inset row in a table
def insert_in_table(dbname,table_name,columns_names,values,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")

        sql_update_query = """INSERT INTO %s (%s) VALUES('%s');"""
        cursor.execute(sql_update_query % (table_name,columns_names,values))
        mariadbConnection.commit()
        #print("alter table successfully ")
        cursor.close()

    except mariadb.Error as error:
        print("Failed to alter mariadb table", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")

#find value in a table
def find_in_table(dbname,table_name,column_name,search_value,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")
        sql_update_query = """SELECT * FROM %s WHERE %s = '%s'"""
        cursor.execute(sql_update_query % (table_name,column_name,search_value))
        value = cursor.fetchall()
        cursor.close()
        return value

    except mariadb.Error as error:
        print("Failed to get value from the table in mariadb", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")


#пуе value of column in a table
def find_column_in_table(dbname,table_name,column_name,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")
        sql_update_query = """SELECT %s FROM %s"""
        cursor.execute(sql_update_query % (column_name,table_name))
        value = cursor.fetchall()
        cursor.close()
        return value

    except mariadb.Error as error:
        print("Failed to get value from the table in mariadb", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")

#find ьгдешздн value in a table            
def find_in_table_for_list(dbname,table_name,column_name,search_value,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb")
        sql_update_query = """SELECT * FROM %s WHERE (%s) = %s"""
        cursor.execute(sql_update_query % (table_name,column_name,search_value))
        value = cursor.fetchall()
        cursor.close()
        return value

    except mariadb.Error as error:
        print("Failed to get value from the table in mariadb", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")
#we are deleting row from table
def delete_row_in_table(dbname,table_name,column_name,search_value,ip,user,password):
    try:
        mariadbConnection = connection_to_db(ip,dbname,user,password)
        cursor = mariadbConnection.cursor()
        #print("Connected to mariadb for deleting")
        sql_update_query = """DELETE FROM %s WHERE %s = '%s'"""
        cursor.execute(sql_update_query % (table_name,column_name,search_value))
        mariadbConnection.commit()
        #print("Deleting is successfully")
        cursor.close()

    except mariadb.Error as error:
        print("Failed to DELETE value from the table in mariadb", error)
    finally:
        if mariadbConnection:
            mariadbConnection.close()
            #print("The mariadb connection is closed")
