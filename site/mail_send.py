from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import re
from flask_mail import Mail, Message
import utils
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import re
from flask_mail import Mail, Message
import utils
import pymongo
from sqlalchemy import create_engine, MetaData, Table
import smtplib
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
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

url = "mongodb://localhost:27017/"
db_name = "mydatabase"
collection_name = "customers5"
data = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Hannah", "address": "Mountain 21"},
  { "name": "Michael", "address": "Valley 345"},
  { "name": "Sandy", "address": "Ocean blvd 2"},
  { "name": "Betty", "address": "Green Grass 1"},
  { "name": "Richard", "address": "Sky st 331"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"},
  { "name": "test", "address": "toto 1633"},
  { "name": "test", "address": "tata 1633"},
  { "name": "test", "address": "titi 1633"},
  { "name": "test", "address": "nono 1633"},
  { "name": "test", "address": "zob 1633"}
]
myquery = {"address": "zob 1633"}
status = "0"
list_status = ["0","1","2"]
sender_address = ''

db_name = ''
password = ''
mail_server = ''

if status == "0":
	nb_days = utils.get_nb_days(db_name, status)
	msg_body = 'toto'
	msg_object = 'test'
	nb_days = utils.get_nb_days(db_name, status)
	utils.newsletter_flow(nb_days,db_name,status,list_status,msg_body,msg_object,password,mail_server,sender_address,db)