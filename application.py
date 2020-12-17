from datetime import time
from flask import Flask, render_template, redirect, request
import backend.sql as SQ
import backend.matching as MC
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        users = SQ.get_volunteer_user_pass()
        tmp = False
        for user in users:
            if (int (phone) == int (user[0]) and password == user[1]): 
                tmp = True
                (phone, zipcode) = SQ.get_volunteer_zip(phone)
                info = MC.match(phone, zipcode)
                for one in info:
                    SQ.assign_request(phone, one[0], zipcode, False)
                return render_template("home.html", vtr=phone, info=SQ.get_requests_for_volunteer(phone))
        if tmp == False:
            return render_template('login.html', flag=True)
    else:
        return render_template('login.html', flag=False)

@app.route("/accept/<string:vtr>/<string:rqstr>", methods=['POST', 'GET'])
def accept(vtr,rqstr):
    if request.method == 'POST':
        (rqid,) = SQ.get_req_id(vtr,rqstr)
        timeperiod = request.form['delivery']
        SQ.accept_request(rqid, timeperiod)
        return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))
    else:
        return render_template('accept.html', vtr=vtr, rqstr=rqstr)

@app.route("/decline/<string:vtr>/<string:rqstr>")
def decline(vtr, rqstr):
    (rqid,) = SQ.get_req_id(vtr,rqstr)
    SQ.decline_request(rqid)
    return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))

@app.route("/requesters", methods=['POST', 'GET'])
def elderly():
    return render_template("requesters.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        name = request.form['name']
        zipcode = int (request.form['zipcode'])
        SQ.register_volunteer(phone, password, name, zipcode)
        info = MC.match(phone, zipcode)
        for one in info:
                SQ.assign_request(phone, one[0], zipcode, False)
        return render_template("home.html", vtr=phone, info=SQ.get_requests_for_volunteer(phone))
    else:
        return render_template("register.html")

@app.route("/termsconditions")
def termsconditions():
    return render_template("termsconditions.html")

@app.route("/settings/<string:vtr>", methods=['POST', 'GET'])
def settings(vtr):
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        pw = request.form['password']
        name = request.form['name']
        info = []
        if (zipcode != ""):
            SQ.update_vtr_zip(zipcode,vtr)
            info = MC.match(vtr, zipcode)
        if (pw != ""):
            SQ.update_vtr_pw(pw, vtr)
        if (name != ""):
            SQ.update_vtr_name(name, vtr)
        if info != []:
            return render_template("home.html", vtr=vtr, info=info)
        else:
            return render_template("home.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))
    else:
        return render_template("settings.html", vtr=vtr, info=SQ.get_requests_for_volunteer(vtr))

if __name__ == "__main__":
    app.run(use_reloader = True, debug=True)