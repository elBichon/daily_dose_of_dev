from flask_mail import Mail, Message
from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import re
import utils
from sqlalchemy import create_engine, MetaData, Table
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
import credentials


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

status = "0"
list_status = ["0","1","2"]
sender_address = credentials.email
db_name = credentials.url
password = credentials.password
mail_server = credentials.mail_server

print(credentials.collection)

myclient = pymongo.MongoClient(credentials.mongourl)
mydb = myclient[credentials.mongodb]
mycol = mydb[credentials.collection]

mylist = [
  { "id": 1,"name": "Amy", "address": "Apple st 652"},
  { "id": 2,"name": "Hannah", "address": "Mountain 21"},
  { "id": 3,"name": "Michael", "address": "Valley 345"},
  { "id": 4,"name": "Sandy", "address": "Ocean blvd 2"},
  { "id": 5,"name": "Betty", "address": "Green Grass 1"},
  { "id": 6,"name": "Richard", "address": "Sky st 331"},
  { "id": 7,"name": "Susan", "address": "One way 98"},
  { "id": 8,"name": "Vicky", "address": "Yellow Garden 2"},
  { "id": 9,"name": "Ben", "address": "Park Lane 38"},
  { "id": 10,"name": "William", "address": "Central st 954"},
  { "id": 11,"name": "Chuck", "address": "Main Road 989"},
  { "id": 12,"name": "Viola", "address": "Sideway 1633"}
]

x = mycol.insert_many(mylist)

#print(x.inserted_ids) 

utils.send_newsletter(mycol,users,db_name,status,list_status,password,mail_server,sender_address,db)
