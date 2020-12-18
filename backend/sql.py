import mysql.connector

con = mysql.connector.connect(
  host="localhost",
  port="3306",
  user="root",
  password="julie123!", #TODO CHANGE
  auth_plugin='mysql_native_password'
)
cursor = con.cursor(buffered=True)

def initialize():
    cursor.execute("DROP DATABASE IF EXISTS db; ")
    cursor.execute("CREATE DATABASE db CHARACTER SET utf8 COLLATE utf8_general_ci; ")
    cursor.execute("USE db; ")

    # vtrPhone, password, name, zip
    cursor.execute("CREATE TABLE volunteers (vtrPhone varchar(20) PRIMARY KEY, password varchar(255) NOT NULL, name varchar(255) NOT NULL, zip int(5) NOT NULL); ")

    # rqstrPhone, name, address, zip, rqDetails, dropDetails, addInfo, thankYou, assigned
    cursor.execute("CREATE TABLE requesters (rqstrPhone varchar(20) PRIMARY KEY, name varchar(255) NOT NULL, address varchar(255) NOT NULL, zip int(5) NOT NULL, rqDetails varchar(1024) NOT NULL, dropDetails varchar(1024) NOT NULL, addInfo varchar(1024), thankYou varchar(1024), assigned boolean NOT NULL, accepted boolean NOT NULL); ")
    # reID, vtrPhone, rqstrPhone, zip, accepted, delivery_time
    cursor.execute("CREATE TABLE requests (rqID int AUTO_INCREMENT PRIMARY KEY, vtrPhone varchar(20) NOT NULL, rqstrPhone varchar(20) NOT NULL, zip int(5) NOT NULL, accepted boolean NOT NULL, delivery_time varchar(256)); ")
    con.commit()

# register a volunteer
def register_volunteer (phone, password, name, zipC):
    sql = "INSERT INTO volunteers (vtrPhone, password, name, zip) VALUES (%s, %s, %s, %s); "
    val = (phone, password, name, zipC)
    cursor.execute(sql,val)
    con.commit()

# add a requester
def add_requester (phone, name, address, zipC, rqDetails, dropDetails, addInfo, thankYou, assigned=False, accepted=False):
    sql = "INSERT INTO requesters (rqstrPhone, name, address, zip, rqDetails, dropDetails, addInfo, thankYou, assigned, accepted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
    val = (phone, name, address, zipC, rqDetails, dropDetails, addInfo, thankYou, assigned, accepted)
    cursor.execute(sql,val)
    con.commit()

def update_vtr_zip (zipCode, vtrPhone):
    sql = "UPDATE volunteers SET zip = %s WHERE vtrPhone = %s; "
    val = (zipCode, vtrPhone)
    cursor.execute(sql, val)
    sql = "UPDATE requesters SET assigned = False, accepted = False where rqstrPhone in (SELECT rqstrPhone FROM requests where vtrPhone = %s) ; "
    cursor.execute(sql % vtrPhone)
    sql = "DELETE FROM requests WHERE vtrPhone = %s; "
    cursor.execute(sql % vtrPhone)

def update_vtr_name (name, vtrPhone):
    sql = "UPDATE volunteers set name = %s WHERE vtrPhone = %s; "
    val = (name, vtrPhone)
    cursor.execute(sql, val)

def update_vtr_pw (password, vtrPhone):
    sql = "UPDATE volunteers set password = %s WHERE vtrPhone = %s; "
    val = (password, vtrPhone)
    cursor.execute(sql, val)

# assign a volunteer to a requester
def assign_request (vtrPhone, rqstrPhone, zipC, accepted=False):
    sql = "INSERT INTO requests (vtrPhone, rqstrPhone, zip, accepted) VALUES (%s, %s, %s, %s); "
    val = (vtrPhone, rqstrPhone, zipC, accepted)
    cursor.execute(sql,val) 
    sql = "UPDATE requesters SET assigned = True WHERE rqstrPhone = %s; "
    cursor.execute(sql % rqstrPhone)
    con.commit()

def get_req_name(rqstrPhone):
    sql = "SELECT name FROM requesters WHERE rqstrPhone = %s"
    cursor.execute(sql % rqstrPhone)
    (name,) = cursor.fetchone()
    con.commit()
    return name

def get_vtr_name(vtrPhone):
    sql = "SELECT name FROM volunteers WHERE vtrPhone = %s"
    cursor.execute(sql % vtrPhone)
    (name,) = cursor.fetchone()
    con.commit()
    return name

def get_req_phone (reqID):
    sql = "SELECT rqstrPhone from requests where rqID = %s; "
    cursor.execute(sql % reqID)
    phone = cursor.fetchone()
    con.commit()
    return phone
# request is accepted by volunteer
def accept_request (requestID, delivery_time):
    sql = "UPDATE requests SET accepted = True, delivery_time = %s WHERE rqID = %s; "
    val = (delivery_time, requestID)
    cursor.execute (sql, val)
    (rqPhone,) = get_req_phone(requestID)
    sql = "UPDATE requesters SET accepted = True WHERE rqstrPhone = %s; "
    cursor.execute(sql % rqPhone)
    con.commit()
    
# request is declined by volunteer
def decline_request (requestID):
    sql = "UPDATE requesters SET assigned = False where rqstrPhone = (SELECT rqstrPhone FROM requests where rqID = %s) ; "
    cursor.execute(sql % requestID)
    sql = "DELETE FROM requests WHERE rqID = %s; "
    cursor.execute(sql % requestID)
    con.commit()

# get info of all requests assigned to volunteer
def get_requests_for_volunteer (vtrPhone):
    sql = "SELECT * FROM requesters WHERE rqstrPhone IN (SELECT rqstrPhone FROM requests WHERE vtrPhone = %s); "
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
    sql = "SELECT * FROM requests; "
    cursor.execute(sql)
    rqs = cursor.fetchall()
    con.commit()
    return rqs

# get all requests
def get_requester_info(rqPhone):
    sql = "SELECT * FROM requesters WHERE rqstrPhone = %s; "
    cursor.execute(sql % rqPhone)
    rqs = cursor.fetchall()
    con.commit()
    return rqs

# get all requesters
def get_requesters():
    sql = "SELECT * FROM requesters; "
    cursor.execute(sql)
    rqstrs = cursor.fetchall()
    con.commit()
    return rqstrs

def get_requester_phones_and_zips():
    sql = "SELECT rqstrPhone, zip from requesters WHERE assigned = 0; "
    cursor.execute(sql)
    info = cursor.fetchall()
    con.commit()
    return info
# get all volunteers
def get_volunteers():
    sql = "SELECT * FROM volunteers; "
    cursor.execute(sql)
    vtrs = cursor.fetchall()
    con.commit()
    return vtrs

# get zip for volunteer phone
def get_volunteer_zip(vtrPhone):
    sql = "SELECT vtrPhone, zip FROM volunteers WHERE vtrPhone = %s; "
    cursor.execute(sql % vtrPhone)
    info = cursor.fetchone()
    con.commit()
    return info

def get_req_id(vtrPhone, rqstrPhone):
    sql = "SELECT rqID FROM requests WHERE vtrPhone = %s AND rqstrPhone = %s; "
    val = (vtrPhone, rqstrPhone)
    cursor.execute(sql, val)
    info = cursor.fetchone()
    con.commit()
    return info

# get volunteer username/pw
def get_volunteer_user_pass():
    sql = "SELECT vtrPhone, password FROM volunteers; "
    cursor.execute(sql)
    vtrs = cursor.fetchall()
    con.commit()
    return vtrs
# delete table
def delete(tableName):
    sql = "TRUNCATE TABLE %s; "
    cursor.execute(sql % tableName)

#
# initialize()
cursor.execute("USE db; ")
# #register_volunteer("+18582038211", "abcd", "Julie", "60637")
# register_volunteer("+12223334444", "abcd", "Bhakti", "606")
# add_requester("+13120221224", "Vernon", "5500 S University Avenue, Chicago, IL", 60637, "trader joe’s frozen pizza, $10", "front door", "no", "thank you for helping me!")
# #add_requester("+13125238576", "Cole", "12100 S Cornell Ave, Chicago, IL", 60637, "milk, 4 cartons", "front door", "please ring the doorbell!", "thank you for being so kind and helping me out!")
# add_requester("+18382776372", "Elizabeth", "3775 Bloomington Drive", 90027, "Broccoli about 2 pounds, milk 8 gallons, french bread, cheese", "no requirement", "no", "It's really generous of you")
# add_requester("+18582721172", "Elif", "408 Mulholland Drive", 90027, "Beef 3 pounds, pork 2 pounds, and about a week of vegetable", "no", "no", "Thanks for your kindness")
# add_requester("+13128443122", "Amy", "4200 S Dorchester Ave, Chicago, IL", 60637, "1kg apples", "please leave it on the doorstep", "no", "thank you for taking time out of your day to help me!")
# add_requester("+13261728944", "Zhimin", "4779 N Cambridge Ave, Chicago", 60637, "buying a chipotle burrito with beef and cheese. It will be about 10 dollars", "entry access is not required", "no", "Thanks!")