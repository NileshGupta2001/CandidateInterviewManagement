#copy of app.py(main)... to see if sessions work
from datetime import datetime
from datetime import date
from flask import Flask, render_template,flash,session,redirect,url_for
import json
from flask import request,jsonify
from flask_session import Session
from flask_mail import *  
from random import *
import mysql.connector
from mysql.connector import errorcode

#today = date.today()
currentDateTime = datetime.now()
today = currentDateTime.date()
app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Session(app)
mail = Mail(app) 
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'nileshgupta2001@gmail.com'  
app.config['MAIL_PASSWORD'] = 'idvbrbrwsndlowft'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)  
otp = randint(000000,999999)
 
@app.route('/')
def index():
  return render_template('index.html')
  
@app.route('/HRreg')  
def HRreg():
  return render_template('HRreg.html')
  
@app.route('/newinterview')  
def newinterview():
  return render_template('newinterview.html')
  
@app.route('/executeint')  
def executeint():
  return render_template('executeint.html')  
  
@app.route('/hrafterlogin')  
def hrafterlogin():
  return render_template('hrafterlogin.html')
  
@app.route('/verify')  
def verify():
  return render_template('verify.html')
  
@app.route('/validate')  
def validate():
  return render_template('validate.html')
  
@app.route('/forpass',methods=["POST","GET"])   
def forpass():  
    print("Content-Type: text/html")
    print()
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        
        if request.method=='POST':
            pwd=request.form.get("pwd", False)  
            conpwd=request.form.get("conpwd", False)  
            if not pwd or not conpwd:
                error_statement="All Form Fields With '*' Are Required."
                return render_template('fail.html', error_statement=error_statement)
            digi = True if next((chr for chr in pwd if chr.isdigit()), None) else False
            if len(pwd)<8 or digi==False:
                error_statement="Incorrect Password Format. Password must have a minimum length of 8 and must contain a digit. "
                return render_template('fail.html', error_statement=error_statement)
            if pwd!=conpwd:
                error_statement="Passwords do not match. Please enter again. "
                return render_template('fail.html', error_statement=error_statement)
            cur.execute("update `HR_login` set `pwd`=%s where `email`=%s",(pwd,hr_email))
            con.commit()
            
            cur.close()
            con.close()
    flash('Your Password has been successfully updated.')
    return render_template('forpass.html')  

@app.route('/validate',methods=["POST","GET"])   
def otp_check():  
    if request.method=='POST':
        user_otp=request.form.get("otp", False)    
        if otp == int(user_otp):  
            return redirect(url_for('forpass')) 
        else:
            flash('Invalid OTP. Email Verification incomplete.')            
            return redirect(url_for('verify'))

    
@app.route('/verify',methods=["POST","GET"])  
def verifymail():
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
    
        if request.method=='POST':
            global hr_email
            hr_email=request.form.get("email", False)
            sql = "SELECT * FROM `HR_login` WHERE `email` = %s"
            cur.execute(sql,(hr_email,))
            cur=cur.fetchall()
            print(cur)
            if len(cur)==1:
                msg = Message('OTP',sender = 'nileshgupta2001@gmail.com', recipients = [hr_email])  
                msg.body = str(otp)  
                mail.send(msg)
                return redirect(url_for('validate'))
            else:
                flash('Email not registered')
                return redirect(url_for('verify'))
                            
@app.route('/hrsuc',methods=["POST","GET"])  
def hrsuc():
    print("Content-Type: text/html")
    print()
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()

        if request.method=='POST':
            signup_HR=request.form
            username=signup_HR['username']
            email=signup_HR['email']
            pwd=signup_HR['pwd']
            conpwd=signup_HR['conpwd']
            if not username or not email or not pwd:
                error_statement="All Form Fields With '*' Are Required."
                return render_template('fail.html', error_statement=error_statement)
            digi = True if next((chr for chr in pwd if chr.isdigit()), None) else False
            if len(pwd)<8 or digi==False:
                error_statement="Incorrect Password Format. Password must have a minimum length of 8 and must contain a digit. "
                return render_template('fail.html', error_statement=error_statement)
            if pwd!=conpwd:
                error_statement="Passwords do not match. Please enter again. "
                return render_template('fail.html', error_statement=error_statement)
            cur.execute("insert into HR_login(username,email,pwd) values(%s,%s,%s)",(username,email,pwd))
            con.commit()

            cur.close()
            con.close()
    return render_template('hrsuc.html')
    
@app.route('/panel')  
def panel():
  return render_template('panel.html')
  
@app.route("/searchpanelbyname",methods=["POST","GET"])
def searchpanelbyname():
    print("Content-Type: text/html")
    print()
    panel=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `panel` ORDER BY `panelID`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                panel = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `panel` WHERE `panelName` LIKE %s ORDER BY panelID DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                panel = cur.fetchall()
                print(panel)
                for result in panel:
                    d1 = result[4].strftime("%m/%d/%Y")
                    d2 = result[5].strftime("%m/%d/%Y")
                    content = {'panelID': result[0], 'panelName': result[1], 'panelDesignation': result[2], 'panelSkills': result[3], 'addedOn': result[4], 'modifiedOn': result[5], 'IsActive': result[6]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchpanelbydesignation",methods=["POST","GET"])
def searchpanelbydesignation():
    print("Content-Type: text/html")
    print()
    panel=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `panel` ORDER BY `panelID`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                panel = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `panel` WHERE `panelDesignation` LIKE %s ORDER BY panelID DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                panel = cur.fetchall()
                print(panel)
                for result in panel:
                    d1 = result[4].strftime("%m/%d/%Y")
                    d2 = result[5].strftime("%m/%d/%Y")
                    content = {'panelID': result[0], 'panelName': result[1], 'panelDesignation': result[2], 'panelSkills': result[3], 'addedOn': result[4], 'modifiedOn': result[5], 'IsActive': result[6]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
  
@app.route("/searchpanelall",methods=["POST","GET"])
def searchpanelall():
    print("Content-Type: text/html")
    print()
    panel=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            query = "SELECT * from `panel` ORDER BY `panelID`"
            cur.execute(query)
            numrows = int(cur.rowcount)
            panel = cur.fetchall()
            for result in panel:
                d1 = result[4].strftime("%m/%d/%Y")
                d2 = result[5].strftime("%m/%d/%Y")
                content = {'panelID': result[0], 'panelName': result[1], 'panelDesignation': result[2], 'panelSkills': result[3], 'addedOn': result[4], 'modifiedOn': result[5], 'IsActive': result[6]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)  
  
@app.route("/table_update",methods=["POST","GET"])
def table_update():
    msg=''
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            table=request.form['table']
            if(table=='panel'):
                string = request.form['string']
                signup1=request.form
                panelName=signup1['panelName']
                panelDesignation=signup1['panelDesignation']
                panelSkills=signup1['panelSkills']
                isActive=signup1['isActive']
                d1 = today.strftime("%Y/%m/%d")
                if not panelName or not panelDesignation or not panelSkills or not isActive:
                    msg="Update Failed. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                print(string)
                cur.execute("UPDATE `panel` SET `panelName` = %s, `panelDesignation` = %s, `panelSkills` = %s, `IsActive` = %s, `ModifiedOn`= %s   WHERE `panelID` = %s ", [panelName, panelDesignation, panelSkills, isActive, d1,string])
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Updated. Reloading the page...'  
            elif(table=='candidate'):
                string = request.form['string']
                signup1=request.form
                username=signup1['username']
                dob=signup1['dob']
                email=signup1['email']
                gender=signup1['gender']
                mobile=signup1['mobile']
                if not username or not email or not gender:
                    msg="Update Failed. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                print(string)
                cur.execute("UPDATE `candidate` SET `username` = %s, `dob` = %s, `email` = %s, `gender` = %s, `mobile` = %s WHERE `userid` = %s ", [username, dob, email, gender, mobile,string])
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Updated. Reloading the page...'
        
            elif(table=='HR_login'):
                string = request.form['string']
                signup1=request.form
                username=signup1['username']
                pwd=signup1['pwd']
                email=signup1['email']
                conpwd=signup1['conpwd']
                if not username or not email or not pwd or not conpwd:
                    msg="Update Failed. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                if pwd!=conpwd:
                    msg="Passwords do not match. Please enter again. "
                    return jsonify(msg)
                print(string)
                cur.execute("UPDATE `HR_login` SET `username` = %s, `email` = %s, `pwd` = %s WHERE `HR_id` = %s ", [username, email, pwd, string])
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Updated. Reloading the page...'
            elif(table=='test'):
                string = request.form['string']
                signup1=request.form
                testName=signup1['testName']
                testSkill=signup1['testSkill']
                testLevel=signup1['testLevel']
                testWeightage=signup1['testWeightage']
                questionCount=signup1['questionCount']
                if not testName or not testWeightage or not testSkill or not testLevel or not questionCount:
                    msg="Error. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                print(string)
                cur.execute("UPDATE `test` SET `testName` = %s, `testSkill` = %s, `testLevel` = %s, `testWeightage` = %s, `questionCount`= %s   WHERE `testID` = %s ", [testName, testSkill, testLevel, testWeightage, questionCount,string])
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Updated. Reloading the page...'
            elif(table=='sched_interview'):
                string = request.form['string']
                signup1=request.form
                role=signup1['role']
                skills = request.form['skills']   
                testName = request.form['testName']
                panel = request.form['panelName']
                if not role or not testName or not panel:
                    msg="Update Failed. All Form Fields With '*' Are Required."
                    return jsonify(msg) 
                cur.execute("UPDATE `sched_interview` SET `role` = %s, `skills` = %s, `testName` = %s, `panel` = %s WHERE `int_id` = %s ", [role, skills, testName, panel, string])
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Updated. Reloading the page...'   
            else:
                msg= 'Error.'
        return jsonify(msg)  
  
  
@app.route('/cand')  
def cand():
    return render_template('cand.html')
    
@app.route('/execute')  
def execute():
    return render_template('execute.html')
  
@app.route("/searchcand",methods=["POST","GET"])
def searchcand():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `candidate` ORDER BY `userid`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `candidate` WHERE `username` LIKE %s ORDER BY userid DESC LIMIT 20",(search_word,))
            #cur.execute("SELECT * from `candidate` WHERE `username` LIKE '%{}%' OR `email` LIKE '%{}%' OR `dob` LIKE '%{}%' OR `gender` LIKE '%{}%' OR `mobile` LIKE '%{}%' ORDER BY id DESC LIMIT 20",(search_word,search_word,search_word,search_word,search_word))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
                for result in candidate:
                    d = result[2].strftime("%m/%d/%Y")
                    content = {'userid': result[0], 'username': result[1], 'dob': d, 'gender': result[4], 'mobile': result[5], 'email': result[3]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    
    #return json.dumps(htmlresponse)
    return jsonify(htmlresponse)
    #return jsonify({'htmlresponse': render_template('response.html', candidate=candidate)})  
    #return jsonify({'htmlresponse':  redirect(url_for("cand",htmlresponse=htmlresponse))})

@app.route("/searchcandininter",methods=["POST","GET"])
def searchcandininter():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `candidate` WHERE `username` LIKE %s ORDER BY userid DESC LIMIT 20",(search_word,))
            #cur.execute("SELECT * from `candidate` WHERE `username` LIKE '%{}%' OR `email` LIKE '%{}%' OR `dob` LIKE '%{}%' OR `gender` LIKE '%{}%' OR `mobile` LIKE '%{}%' ORDER BY id DESC LIMIT 20",(search_word,search_word,search_word,search_word,search_word))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'username': result[1], 'mobile': result[5], 'email': result[3]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    
    #return json.dumps(htmlresponse)
    return jsonify(htmlresponse)
    #return jsonify({'htmlresponse': render_template('response.html', candidate=candidate)})  
    #return jsonify({'htmlresponse':  redirect(url_for("cand",htmlresponse=htmlresponse))})    
    
@app.route("/searchcandbymobile",methods=["POST","GET"])
def searchcandbymobile():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `candidate` ORDER BY `userid`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `candidate` WHERE `mobile` LIKE %s ORDER BY userid DESC LIMIT 20",(search_word,))
            #cur.execute("SELECT * from `candidate` WHERE `username` LIKE '%{}%' OR `email` LIKE '%{}%' OR `dob` LIKE '%{}%' OR `gender` LIKE '%{}%' OR `mobile` LIKE '%{}%' ORDER BY id DESC LIMIT 20",(search_word,search_word,search_word,search_word,search_word))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
                for result in candidate:
                    d = result[2].strftime("%m/%d/%Y")
                    content = {'userid': result[0], 'username': result[1], 'dob': d, 'gender': result[4], 'mobile': result[5], 'email': result[3]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchnameforint",methods=["POST","GET"])
def searchnameforint():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)    
            search_word= f"%{search_word}%"
            query = ("SELECT * from `candidate` WHERE `username` LIKE %s ORDER BY userid DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'username': result[1], 'mobile': result[5], 'email': result[3]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchcandbyemail",methods=["POST","GET"])
def searchcandbyemail():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `candidate` ORDER BY `userid`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `candidate` WHERE `email` LIKE %s ORDER BY userid DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
                for result in candidate:
                    d = result[2].strftime("%m/%d/%Y")
                    content = {'userid': result[0], 'username': result[1], 'dob': d, 'gender': result[4], 'mobile': result[5], 'email': result[3]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    

@app.route("/searchcandall",methods=["POST","GET"])
def searchcandall():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query = "SELECT * from `candidate` ORDER BY `userid`"
            cur.execute(query)
            numrows = int(cur.rowcount)
            candidate = cur.fetchall()
            for result in candidate:
                    d = result[2].strftime("%m/%d/%Y")
                    content = {'userid': result[0], 'username': result[1], 'dob': d, 'gender': result[4], 'mobile': result[5], 'email': result[3]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchhrall",methods=["POST","GET"])
def searchhrall():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query = "SELECT * from `HR_login` ORDER BY `HR_id`"
            cur.execute(query)
            numrows = int(cur.rowcount)
            candidate = cur.fetchall()
            for result in candidate:
                    content = {'HR_id': result[0], 'username': result[1], 'email': result[2]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/searchtestall",methods=["POST","GET"])
def searchtestall():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query = "SELECT * from `test` ORDER BY `testID`"
            cur.execute(query)
            numrows = int(cur.rowcount)
            candidate = cur.fetchall()
            for result in candidate:
                    content = {'testID': result[0], 'testName': result[1], 'testSkill': result[2], 'testLevel': result[3], 'testWeightage': result[4], 'questionCount': result[5]}
                    htmlresponse.append(content)
                    content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/searchintall",methods=["POST","GET"])
def searchintall():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query = "SELECT * from `sched_interview` ORDER BY `int_id`"
            cur.execute(query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                #result[6]=datetime.strptime(result[6],"%d%b%Y%H%M%S")
                #result[6] = result[6].date()
                t = result[6]
                t=t.strftime('%m/%d/%Y')
                content = {'int_id': result[0], 'name': result[1], 'role': result[2], 'skills': result[3], 'testName': result[4], 'panelName': result[5], 'addedOn': t,'Mobile': result[7],'Email': result[8]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchresall",methods=["POST","GET"])
def searchresall():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query = "SELECT * from `result` ORDER BY `res_id`"
            cur.execute(query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                #result[6]=datetime.strptime(result[6],"%d%b%Y%H%M%S")
                #result[6] = result[6].date()
                t = result[6]
                t=t.strftime('%m/%d/%Y')
                content = {'res_id': result[0], 'name': result[1], 'role': result[4], 'skills': result[5],'mobile': result[2],'email': result[3],'marks': result[6] }
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)

@app.route("/searchhrbyemail",methods=["POST","GET"])
def searchhrbyemail():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `hr_login` WHERE `email` LIKE %s ORDER BY HR_id DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'HR_id': result[0], 'username': result[1], 'email': result[2]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    

@app.route("/searchtestbyname",methods=["POST","GET"])
def searchtestbyname():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `test` WHERE `testName` LIKE %s ORDER BY testID DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'testID': result[0], 'testName': result[1], 'testSkill': result[2], 'testLevel': result[3], 'testWeightage': result[4], 'questionCount': result[5]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/searchtestbyskills",methods=["POST","GET"])
def searchtestbyskills():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `test` WHERE `testSkill` LIKE %s ORDER BY testID DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'testID': result[0], 'testName': result[1], 'testSkill': result[2], 'testLevel': result[3], 'testWeightage': result[4], 'questionCount': result[5]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/searchhrbyusername",methods=["POST","GET"])
def searchhrbyusername():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `hr_login` WHERE `username` LIKE %s ORDER BY HR_id DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'HR_id': result[0], 'username': result[1], 'email': result[2]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)

@app.route("/searchintbyname",methods=["POST","GET"])
def searchintbyname():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            search_word= f"%{search_word}%"
            query = ("SELECT * from `sched_interview` WHERE `name` LIKE %s ORDER BY int_id DESC LIMIT 20",(search_word,))
            cur.execute(*query)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                t = result[6]
                t=t.strftime('%m/%d/%Y')
                content = {'int_id': result[0], 'name': result[1], 'role': result[2], 'skills': result[3], 'testName': result[4], 'panelName': result[5], 'addedOn': t,'Mobile': result[7],'Email': result[8]}
                htmlresponse.append(content)
                content = {}
    print(htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/interviewrecords",methods=["POST","GET"])
def interviewrecords():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query1 = ("SELECT * from `panel`")
            cur.execute(query1)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'panelName': result[1]}
                htmlresponse.append(content)
                content = {}
            query2 = ("SELECT * from `test`")
            cur.execute(query2)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'testName': result[1]}
                htmlresponse.append(content)
                content = {}
    print("HTMLRESPONSE: ",htmlresponse)
    return jsonify(htmlresponse) 

@app.route("/execinterviewrecords",methods=["POST","GET"])
def execinterviewrecords():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `sched_interview` ORDER BY `int_id`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `sched_interview` WHERE `name` LIKE %s ORDER BY `int_id` DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
            for result in candidate:
                content = {'int_id': result[0], 'name': result[1], 'role': result[2], 'skills': result[3], 'Mobile': result[7],'Email': result[8]}
                htmlresponse.append(content)
                content = {}
    print("HTMLRESPONSE: ",htmlresponse)
    return jsonify(htmlresponse)     
    
@app.route("/searchintbymobile",methods=["POST","GET"])
def searchintbymobile():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `sched_interview` ORDER BY `int_id`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `sched_interview` WHERE `Mobile` LIKE %s ORDER BY `int_id` DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
            for result in candidate:
                content = {'int_id': result[0], 'name': result[1], 'role': result[2], 'skills': result[3], 'Mobile': result[7],'Email': result[8]}
                htmlresponse.append(content)
                content = {}
    print("HTMLRESPONSE: ",htmlresponse)
    return jsonify(htmlresponse)
    
@app.route("/searchintbyemail",methods=["POST","GET"])
def searchintbyemail():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            search_word = request.form.get("query", False)
            print(search_word)
            if search_word == ' ':
                query = "SELECT * from `sched_interview` ORDER BY `int_id`"
                cur.execute(query)
                numrows = int(cur.rowcount)
                candidate = cur.fetchall()
            else:    
                search_word= f"%{search_word}%"
                query = ("SELECT * from `sched_interview` WHERE `email` LIKE %s ORDER BY `int_id` DESC LIMIT 20",(search_word,))
                cur.execute(*query)
                candidate = cur.fetchall()
                print(candidate)
            for result in candidate:
                content = {'int_id': result[0], 'name': result[1], 'role': result[2], 'skills': result[3], 'Mobile': result[7],'Email': result[8]}
                htmlresponse.append(content)
                content = {}
    print("HTMLRESPONSE: ",htmlresponse)
    return jsonify(htmlresponse)
    
    
@app.route("/schedulerecords",methods=["POST","GET"])
def schedulerecords():
    print("Content-Type: text/html")
    print()
    candidate=" "
    htmlresponse=[]
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            query1 = ("SELECT * from `sched_interview`")
            cur.execute(query1)
            candidate = cur.fetchall()
            print(candidate)
            for result in candidate:
                content = {'name': result[1],'role': result[2], 'mobile': result[7],'email': result[8],'skills': result[3]}
                htmlresponse.append(content)
                content = {}
    print("HTMLRESPONSE: ",htmlresponse)
    return jsonify(htmlresponse)    
    
@app.route("/cand_add",methods=["POST","GET"])
def cand_add():
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            table=request.form['table']
            if(table=='candidate'):
                signup1=request.form
                username=signup1['username']
                dob=signup1['dob']
                email=signup1['email']
                gender=signup1['gender']
                mobile=signup1['mobile']
                if not username or not email or not gender:
                    msg="Error. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                cur.execute("insert into candidate(username,dob,email,gender,mobile) values(%s,%s,%s,%s,%s)",(username,dob,email,gender,mobile))
                con.commit()
                con.commit()
                cur.close()
                con.close()
                msg = 'Record successfully Added. Please reload.'  
            
            elif(table=='panel'):
                signup1=request.form
                panelName=signup1['panelName']
                panelDesignation=signup1['panelDesignation']
                panelSkills=signup1['panelSkills']
                isActive=signup1['IsActive']
                d1 = today.strftime("%Y/%m/%d")
                if not panelName or not panelDesignation or not panelSkills or not isActive:
                    msg="Error. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                    
                cur.execute("insert into panel(panelName,panelDesignation,panelSkills,IsActive,AddedOn,ModifiedOn) values(%s,%s,%s,%s,%s,%s)",(panelName,panelDesignation,panelSkills,isActive,d1,d1))
                con.commit()
                cur.close()
                con.close()
                msg = 'Record successfully Added. Please reload.'
                
            elif(table=='HR_login'):
                signup1=request.form
                username=signup1['username']
                email=signup1['email']
                pwd=signup1['pwd']
                conpwd=signup1['conpwd']
                if not username or not email or not pwd or not conpwd:
                    msg="Error. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                if pwd!=conpwd:
                    msg="Passwords do not match. Please enter again. "
                    return jsonify(msg)
                cur.execute("insert into HR_login(username,email,pwd) values(%s,%s,%s)",(username,email,pwd,))
                con.commit()
                cur.close()
                con.close()
                msg = 'Record successfully Added. Please reload.'
                
            elif(table=='test'):
                signup1=request.form
                testName=signup1['testName']
                testSkill=signup1['testSkill']
                testLevel=signup1['testLevel']
                testWeightage=signup1['testWeightage']
                questionCount=signup1['questionCount']
                d1 = today.strftime("%Y/%m/%d")
                if not testName or not testWeightage or not testSkill or not testLevel or not questionCount:
                    msg="Error. All Form Fields With '*' Are Required."
                    return jsonify(msg)
                    
                cur.execute("insert into test(testName,testSkill,testLevel,testWeightage,questionCount,AddedOn) values(%s,%s,%s,%s,%s,%s)",(testName,testSkill,testLevel,testWeightage,questionCount,d1))
                con.commit()
                cur.close()
                con.close()
                msg = 'Record successfully Added. Please reload.'
                
            elif(table=='sched_interview'):
                signup1=request.form
                name=signup1['name']
                role=signup1['role']
                mobile=signup1['mobile']
                email=signup1['email']
                print("Name:",name)
                skills = request.form['skills']
                print("Skills: ",skills)
                testName = request.form['testName']
                panel = request.form['panelName']
                if not name or not role or not testName or not panel or not testName or not skills:
                    msg="Error .All Form Fields With '*' Are Required."
                    return jsonify(msg) 
                cur.execute("insert into sched_interview(name,mobile,email,role,skills,testName,panel,addedOn) values(%s,%s,%s,%s,%s,%s,%s,%s)",(name,mobile,email,role,skills,testName,panel,today))
                con.commit()

                cur.close()
                con.close()
                msg = 'Record successfully Added. Reloading the page...'     
    
            else:
                msg="error."
    return jsonify(msg)    

@app.route("/cand_delete",methods=["POST","GET"])
def cand_delete():
    msg=""
    try:
        con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cur=con.cursor()
        print("Connection established")
        if request.method == 'POST':
            table= request.form['table']
            if(table=='candidate'):
                getid = request.form['string']
                print(getid)
                cur.execute("DELETE FROM `candidate` WHERE `userid` = %s",[getid])
                msg = 'Record deleted successfully'   
            elif(table=='panel'):
                getid = request.form['string']
                print(getid)
                cur.execute("DELETE FROM `panel` WHERE `panelID` = %s",[getid])
                msg = 'Record deleted successfully'
            elif(table=='HR_login'):
                getid = request.form['string']
                print(getid)
                cur.execute("DELETE FROM `HR_login` WHERE `HR_id` = %s",[getid])
                msg = 'Record deleted successfully'    
            elif(table=='test'):
                getid = request.form['string']
                print(getid)
                cur.execute("DELETE FROM `test` WHERE `testID` = %s",[getid])
                msg = 'Record deleted successfully'   
            elif(table=='sched_interview'):    
                getid = request.form['string']
                print(getid)
                cur.execute("DELETE FROM `sched_interview` WHERE `int_id` = %s",[getid])
                msg = 'Record deleted successfully'
            else:
                msg="error"
        con.commit()

        cur.close()
        con.close()   
    return jsonify(msg) 
    
  
@app.route('/test')  
def test():
  return render_template('test.html')

@app.route('/customerreg')  
def customerreg():
  return render_template('customerreg.html')

@app.route('/interview')  
def interview():
    return render_template('interview.html')
  
@app.route('/dashboard')  
def dashboard():

    #if not session.get("name"):
        # if not there in the session then redirect to the login page
        #return redirect("/login")
    return render_template('dashboard.html')
      
@app.route("/",methods=["POST"])  
def checklogin():     
  try:
    con = mysql.connector.connect(user="nilesh", password="NewPass@21", host="registerdbnew.mysql.database.azure.com", port=3306, database="candidate_interview",  ssl_ca=r"C:\Users\dell\Downloads\BaltimoreCyberTrustRoot.crt.pem",ssl_disabled=False)
    print("Connection established")
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with the user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
  else:
    cur=con.cursor()
    signin=request.form
    email=signin['email']
    pwd=signin['pwd']
    if not email:
        error_statement="Email is required"
        return render_template('fail.html', error_statement=error_statement)
    if not pwd:
        error_statement="Password is required"
        return render_template('fail.html', error_statement=error_statement)

    sql = "SELECT * FROM `HR_login` WHERE `email` = %s AND `pwd` =%s"

    cur.execute(sql, (email, pwd))
    #rows=cur.execute("select email,pwd from candidate where email={a} and pwd={b}".format(a=email,b=pwd))
    cur=cur.fetchall()
    print(cur)
    if len(cur)==1:
        username=cur[0][1]
        session["name"]=username
        #flash('Logged in successfully as')
        return render_template('dashboard.html',username=username)
    else:
        flash('Invalid Username and password. Please try again.')
        return render_template('index.html',email=email)
        
                  
@app.route("/logout")
def logout():
    session["name"] = None
    return render_template('logout.html')

if __name__ == '__main__':
  app.run(debug=True)