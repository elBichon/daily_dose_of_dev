from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import re
import pymongo
from sqlalchemy import create_engine, MetaData, Table
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import update
import credentials
print(credentials.mongodb)
app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = credentials.url
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)
class users(db.Model):
	_id = db.Column("id",db.Integer, primary_key = True)
	email = db.Column(db.String(100))
	status = db.Column(db.Integer)
	nb_day =  db.Column(db.Integer)

	def __init__(self, email, status, nb_day):
		self.email = email
		self.status = status
		self.nb_day = nb_day

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER = credentials.mail_server,
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USE_TLS = False,
	MAIL_USERNAME = credentials.email,
	MAIL_PASSWORD = credentials.password
	)
mail = Mail(app)

myclient = pymongo.MongoClient(credentials.mongourl)
mydb = myclient[credentials.mongodb]
mycol = mydb[credentials.collection]

def check_email(user):
	try:
		if isinstance(user, str) == True and len(user) > 0 and bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", user)) == True:
			return True
		else: 
			return False
	except:
		return False

def check_status(status,list_status):
	try:
		if status in list_status:
			return True
		else:
			return False
	except:
		return False

def check_nb_days(nb_day):
	try:
		if nb_day == "0":
			return True
		else:
			return False
	except:
		return False

def insert_user(agree,found_user,users,user,status,nb_day,db):
	try:		
		if found_user:
			session["email"] = found_user.email
			flash("Your email is already in the database","info")
			return False
		else:
			usr = users(user,status,nb_day,agree)
			db.session.add(usr)
			db.session.commit()
			flash("Your email has been added, you will receive a confirmation email. You may have to check your spam folder","info")
			return True
	except:
		return False

def update_query(db,users,message,user,status):
	try:
		if isinstance(message, str) == True and len(message) > 0:
			query = users.query.filter_by(email=str(user)).update(dict(status=status))
			db.session.commit()
			flash(message,"info")
			return render_template("update_account.html")
	except:
		return False

def pick_query(found_user,status,db,users,user,sender_address):
	try:
		if status == "1":
			message = "Your account has been updated to a free account, thank you, check your email for a confirmation from our side please"
			msg_body = "update to free account"
			msg_object = "free"
			update_query(db,users,message,user,status)
			flask_email(user,sender_address,msg_body,msg_object)
		elif status == "2":
			message = "Your account has been updated to a premium account, thank you, check your email for a confirmation from our side please"
			msg_body = "update to premium account"
			msg_object = "premium"
			update_query(db,users,message,user,status)
			flask_email(user,sender_address,msg_body,msg_object)
		elif status == "3":
			message = "Your account has been paused for now, thank you, check your email for a confirmation from our side please"
			msg_body = "update to pause account"
			msg_object = "pause"
			update_query(db,users,message,user,status)
			flask_email(user,sender_address,msg_body,msg_object)
		elif status == "4":
			msg_body = "update to delete account"
			msg_object = "delete"
			flash("Your account has been deleted, thank you, check your email for a confirmation from our side","info")
			db.session.delete(found_user)
			db.session.commit()
			flask_email(user,sender_address,msg_body,msg_object)
			return render_template("update_account.html")	
	except:
		return False

def update_account(db,users,user,status,sender_address):
	try:
		if check_email(user) == True and check_status(status,["1","2","3","4"]) == True:
			found_user = users.query.filter_by(email=user).first()
			if found_user:
				pick_query(found_user,status,db,users,user,sender_address)
			else:
				flash("Something went wrong, try again, if it fails, please contact the admin","info")
				return render_template("update_account.html")	
		else:
			flash("Something went wrong, try again, if it fails, please contact the admin","info")
			return render_template("update_account.html")
	except:
		return False	

def flask_email(user,sender_address,msg_body,msg_object):
	try:
		if check_email(user) == True and check_email(sender_address) == True:
			msg = Message(msg_object, sender = sender_address, recipients = [user])
			msg.body = msg_body
			mail.send(msg)
		else:
			return False
	except:
		pass

def create_mongo_db(url,db_name,collection_name):
	try:
		if isinstance(url, str) == True and len(url) > 0 and isinstance(db_name, str) == True and len(db_name) > 0 and isinstance(collection_name, str) == True and len(collection_name) > 0:
			myclient = pymongo.MongoClient(url)
			mydb = myclient[db_name]
			dblist = myclient.list_database_names()
			mycol = mydb[collection_name]
			collist = mydb.list_collection_names()
			return mycol
		else:
			return False
	except:
		return False

def insert_into_mongo(mycol,data):
	try:
		if isinstance(data, list) == True and len(data) > 0 and isinstance(mycol,pymongo.collection.Collection):
			x = mycol.insert_many(data)
			return True
		else:
			return False
	except:
		return False

def mongodb_creation(url,db_name,collection_name,data):
	try:
		mycol = create_mongo_db(url,db_name,collection_name)
		if mycol != False:
			insert_into_mongo(mycol,data)
		else:
			return False
	except:
		return False


def search_mongo(url,db_name,collection_name,myquery):
	try:
		if isinstance(url, str) == True and len(url) > 0 and isinstance(db_name, str) == True and len(db_name) > 0 and isinstance(collection_name, str) == True and len(collection_name) > 0 and isinstance(myquery, dict) == True and len(myquery) ==1:
			myclient = pymongo.MongoClient(url)
			mydb = myclient[db_name]
			dblist = myclient.list_database_names()
			mycol = mydb[collection_name]
			mydoc = mycol.find(myquery)
			return mydoc
		else:
			return False
	except:
		return False

def get_nb_days(db_name,status):
	try:
		if isinstance(db_name, str) == True and len(db_name) > 0:
			engine = create_engine(db_name, convert_unicode=True)
			metadata = MetaData(bind=engine)
			query = "SELECT DISTINCT nb_day FROM users WHERE status = "+status
			result = engine.execute(query)
			user_list = []
			for _r in result:
				user_list.append(str(_r[0]))
			return user_list
		else:
			return False
	except:
		return False

def get_mail_address(db_name,status,nb_day,list_status):
	try:
		if isinstance(db_name, str) == True and len(db_name) > 0 and check_status(status,list_status) == True and isinstance(nb_day, str) == True and len(nb_day) > 0:
			engine = create_engine(db_name, convert_unicode=True)
			metadata = MetaData(bind=engine)
			query = "SELECT email FROM users WHERE status = "+status+" AND nb_day = "+nb_day
			result = engine.execute(query)
			mail_address = []
			for _r in result:
				mail_address.append(str(_r[0]))
			return mail_address
		else:
			return False
	except:
		return False

def get_status(db_name):
	try:
		if isinstance(db_name, str) == True and len(db_name) > 0:
			engine = create_engine(db_name, convert_unicode=True)
			metadata = MetaData(bind=engine)
			query = "SELECT DISTINCT status FROM users"
			result = engine.execute(query)
			status_list = []
			for _r in result:
				status_list.append(str(_r[0]))
			return status_list
		else:
			return False
	except:
		return False

def send_email(mycol,query,user,sender_address,password,mail_server):
	try:
		if isinstance(sender_address, str) == True and len(sender_address) > 0 and isinstance(password, str) == True and len(password) > 0 and isinstance(mail_server, str) == True and len(mail_server) > 0:
			msg = MIMEMultipart()
			print('===============')
			msg['From'] = sender_address
			mydoc = mycol.find_one(query)
			msg['Subject'] = str(mydoc['name'])
			message = str(mydoc['address'])
			for u in user:
				print(u)
				msg['To'] = u
				msg.attach(MIMEText(message))	
				mailserver = smtplib.SMTP(mail_server, 587)
				mailserver.ehlo()
				mailserver.starttls()
				mailserver.ehlo()
				mailserver.login(sender_address, password)
				mailserver.sendmail(sender_address, u, msg.as_string())
				mailserver.quit()
		else:
			return False
	except:
		return False

def update_nb_days(db_name,user_list,nb_day):
	try:
		if isinstance(db_name, str) == True and len(db_name) > 0 and isinstance(user_list, list) == True and len(user_list) > 0 and isinstance(nb_day, str) == True and len(nb_day) > 0:
			nb_day = str(int(nb_day) + 1)
			for user in user_list:
				query = users.query.filter_by(email=str(user)).update(dict(nb_day=nb_day))
				db.session.commit()
		return True
	except:
		return False

def newsletter_flow(mycol,nb_days,db_name,status,list_status,password,mail_server,sender_address,db):
	for nb_day in nb_days:
		user_list = get_mail_address(db_name,status,nb_day,list_status)
		query = {"id":int(nb_day)}
		send_email(mycol,query,user_list,sender_address,password,mail_server)
		update_nb_days(db_name,user_list,nb_day)

def send_newsletter(mycol,users,db_name,status,list_status,password,mail_server,sender_address,db):
	status_list = get_status(db_name)
	try:
		for status in status_list:
			if status == "0":
				nb_days = get_nb_days(db_name, status)
				newsletter_flow(mycol,nb_days,db_name,status,list_status,password,mail_server,sender_address,db)
			elif status == "1":
				nb_days = get_nb_days(db_name,status)
				newsletter_flow(mycol,nb_days,db_name,status,list_status,password,mail_server,sender_address,db)
			elif status == "2":
				nb_days = get_nb_days(db_name,status)
				newsletter_flow(mycol,nb_days,db_name,status,list_status,password,mail_server,sender_address,db)
	except:
		pass