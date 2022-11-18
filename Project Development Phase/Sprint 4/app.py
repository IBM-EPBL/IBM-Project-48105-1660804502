from flask import Flask,render_template, request, redirect, url_for, session
import ibm_db

import uuid
import hashlib
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

app= Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'


def sendemail(email,password):

    sg = sendgrid.SendGridAPIClient(api_key="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")
    from_email = Email("rithi.prem03@gmail.com")  
    to_email = To(str(email)) 
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "your username is " + email + " and password is " + password)
    mail = Mail(from_email, to_email, subject, content)

    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=qtv69313;PWD=IcxBMJ7p5ZdS0E29",'','')
app = Flask(__name__)

@app.route("/")
def log():
    return render_template('home.html')


@app.route('/loginn')
def loginn():
  return render_template('login.html')

@app.route('/reques')
def reques():
  return render_template('request.html')

@app.route('/donor')
def donor():
  return render_template('donor.html')

@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/detail')
def detail():
  return render_template('detail.html')

@app.route('/register',methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':

    name = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    age = request.form['age']
    bloodgroup = request.form['bloodgroup']
    address = request.form['place']
    password = request.form['password']
 
    sql = "SELECT * FROM signup WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO signup VALUES (?,?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phone)
      ibm_db.bind_param(prep_stmt, 4, age)
      ibm_db.bind_param(prep_stmt, 5, bloodgroup)
      ibm_db.bind_param(prep_stmt, 6, address)
      ibm_db.bind_param(prep_stmt, 7, password)
      ibm_db.execute(prep_stmt)
    
    return render_template('login.html', msg="Data saved successfuly..Please login using your details")

@app.route('/plasmareq',methods = ['POST', 'GET'])
def plasmareq():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    bloodgroup = request.form['bloodgroup']
    date = request.form['date']
    address = request.form['address']
    district = request.form['district']
    state = request.form['state']
    age = request.form['age']

    insert_sql = "INSERT INTO plasmarequest VALUES (?,?,?,?,?,?,?,?,?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, email)
    ibm_db.bind_param(prep_stmt, 3, phone)
    ibm_db.bind_param(prep_stmt, 4, bloodgroup)
    ibm_db.bind_param(prep_stmt, 5, date)
    ibm_db.bind_param(prep_stmt, 6, address)
    ibm_db.bind_param(prep_stmt, 7, district)
    ibm_db.bind_param(prep_stmt, 8, state)
    ibm_db.bind_param(prep_stmt, 9, age)
    ibm_db.execute(prep_stmt)
    
    return render_template('home.html', msg="Data saved successfuly")


@app.route('/donorform',methods = ['POST', 'GET'])
def donorform():
  if request.method == 'POST':

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    bloodgroup = request.form['bloodgroup']
    date = request.form['date']
    address = request.form['address']
    district = request.form['district']
    state = request.form['state']
    age = request.form['age']

    insert_sql = "INSERT INTO donorform VALUES (?,?,?,?,?,?,?,?,?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, name)
    ibm_db.bind_param(prep_stmt, 2, email)
    ibm_db.bind_param(prep_stmt, 3, phone)
    ibm_db.bind_param(prep_stmt, 4, bloodgroup)
    ibm_db.bind_param(prep_stmt, 5, date)
    ibm_db.bind_param(prep_stmt, 6, address)
    ibm_db.bind_param(prep_stmt, 7, district)
    ibm_db.bind_param(prep_stmt, 8, state)
    ibm_db.bind_param(prep_stmt, 9, age)
    ibm_db.execute(prep_stmt)
    
    return render_template('home.html', msg="Data saved successfuly")

@app.route('/login',methods=['POST','GET'])
def login():
  
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM signup WHERE email =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
            return render_template('detail.html') 
    else:
        return render_template('login.html', msg="Login unsuccessful. Incorrect username / password !")




if __name__ == '__main__':
    app.run()       
       