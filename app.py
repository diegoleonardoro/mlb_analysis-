import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

from flask import (
    Flask,
    render_template,
    jsonify,
    request)



POSTGRES_ADDRESS = 'localhost' 
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres' 
POSTGRES_PASSWORD = 'dd' 
POSTGRES_DBNAME = 'Lahman DB' 


postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,password=POSTGRES_PASSWORD,ipaddress=POSTGRES_ADDRESS,port=POSTGRES_PORT,dbname=POSTGRES_DBNAME))

# create the connection
engine = create_engine(postgres_str)


#create Flask Postgres connection:
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_str

db = SQLAlchemy(app)




#@app.route("/")
#def index():
 #   return render_template("index.html")


