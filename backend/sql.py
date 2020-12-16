import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="root",
  password="", #CHANGE
  auth_plugin='mysql_native_password'
)
cursor = con.cursor()

def initialize():
    cursor.execute("DROP DATABASE IF EXISTS db;")
    cursor.execute("CREATE DATABASE db")
    cursor.execute("USE db")

    # vtrPhone, password, name, zip
    cursor.execute("CREATE TABLE volunteers (vtrPhone int(10) PRIMARY KEY, password varchar(255) NOT NULL, name varchar(255) NOT NULL, zip int(5) NOT NULL); ")

    # rqstrPhone, name, address, zip, rqDetails, dropDetails, addInfo, thankYou, assigned
    cursor.execute("CREATE TABLE requesters (rqstrPhone int(10) PRIMARY KEY, name varchar(255) NOT NULL, address varchar(255) NOT NULL, zip int(5) NOT NULL, rqDetails varchar(1024) NOT NULL, dropDetails varchar(1024) NOT NULL, addInfo varchar(1024), thankYou varchar(1024), assigned boolean NOT NULL) ;")

    # reID, vtrPhone, rqstrPhone, zip, accepted, delivery_time
    cursor.execute("CREATE TABLE requests (rqID int AUTO_INCREMENT PRIMARY KEY, vtrPhone int(10) NOT NULL, rqstrPhone int(10) NOT NULL, zip int(5) NOT NULL, accepted boolean NOT NULL, delivery_time varchar(256)); ")
    con.commit()

# register a volunteer
def register_volunteer (phone, password, name, zipC):
    sql = "INSERT INTO volunteers (vtrPhone, password, name, zip) VALUES (%s, %s, %s, %s); "
    val = (phone, password, name, zipC)
    cursor.execute(sql,val)
    con.commit()

# add a requester
def add_requester (phone, name, address, zipC, rqDetails, dropDetails, addInfo, thankYou, assigned=False):
    sql = "INSERT INTO requesters (rqstrPhone, name, address, zip, rqDetails, dropDetails, addInfo, thankYou, assigned) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); "
    val = (phone, name, address, zipC, rqDetails, dropDetails, addInfo, thankYou, assigned)
    cursor.execute(sql,val)
    con.commit()

# assign a volunteer to a requester
def assign_request (vtrPhone, rqstrPhone, zipC, accepted=False):
    sql = "INSERT INTO requests (vtrPhone, rqstrPhone, zip, accepted) VALUES (%s, %s, %s, %s); "
    val = (vtrPhone, rqstrPhone, zipC, accepted)
    cursor.execute(sql,val) 
    sql = "UPDATE requesters SET assigned = True WHERE rqstrPhone = %s; "
    cursor.execute(sql % rqstrPhone)
    con.commit()

# request is accepted by volunteer
def accept_request (requestID, delivery_time):
    sql = "UPDATE requests SET accepted = True WHERE (rqID = %s, delivery_time = %s)"
    val = (requestID, delivery_time)
    cursor.execute (sql, val)
    con.commit()
    
# request is declined by volunteer
def decline_request (requestID):
    sql = "UPDATE requesters SET assigned = False where rqstrPhone = (SELECT rqstrPhone FROM requests where rqID = %s; "
    cursor.execute(sql % requestID)
    sql = "DELETE FROM requests WHERE rqID = %s; "
    cursor.execute(sql % requestID)
    con.commit()

# get info of all requests assigned to volunteer
def get_requests_for_volunteer (vtrPhone):
    sql = "SELECT * FROM requesters WHERE rqstrPhone = (SELECT rqstrPhone FROM requests WHERE vtrPhone = %s); "
    cursor.execute(sql % vtrPhone)
    info = cursor.fetchall()
    con.commit()
    return info

# get info of volunteer for requester
def get_volunteer_info_for_requester (rqstrPhone):
    sql = "SELECT * FROM volunteers WHERE vtrPhone = (SELECT vtrPhone FROM requests WHERE rqstrPhone = %s); "
    cursor.execute(sql % rqstrPhone)
    info = cursor.fetchall()
    con.commit()
    return info

# delete a volunteer from volunteers table
def delete_volunteer (vtrPhone):
    sql = "UPDATE requesters SET assigned = False where rqstrPhone = (SELECT rqstrPhone FROM requests where vtrPhone = %s); "
    cursor.execute (sql % vtrPhone)
    sql = "DELETE FROM requests WHERE vtrPhone = %s; "
    cursor.execute (sql % vtrPhone)
    sql = "DELETE FROM volunteers WHERE vtrPhone = %s; "
    cursor.execute (sql % vtrPhone)
    con.commit()
    
# delete a requester from requesters table
def delete_requester (rqstrPhone):
    sql = "DELETE FROM requests WHERE rqstrPhone = %s; "
    cursor.execute (sql % rqstrPhone)
    sql = "DELETE FROM requesters WHERE rqstrPhone = %s; "
    cursor.execute (sql % rqstrPhone)
    con.commit()

# delete a request from requests table 
def delete_request (rqID):
    sql = "DELETE FROM requests WHERE rqID = %s; "
    cursor.execute (sql % rqID)
    con.commit()

# get all requests
def get_requests():
    sql = "SELECT * FROM requests"
    cursor.execute(sql)
    rqs = cursor.fetchall()
    con.commit()
    return rqs

# get all requesters
def get_requesters():
    sql = "SELECT * FROM requesters"
    cursor.execute(sql)
    rqstrs = cursor.fetchall()
    con.commit()
    return rqstrs

# get all volunteers
def get_volunteers():
    sql = "SELECT * FROM volunteers"
    cursor.execute(sql)
    vtrs = cursor.fetchall()
    con.commit()
    return vtrs

# delete table
def delete(tableName):
    sql = "TRUNCATE TABLE %s;"
    cursor.execute(sql % tableName)

cursor.close()
con.close()