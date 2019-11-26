import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


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

#reflect an existing database into a new model
Base = automap_base()

#reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
batting = Base.classes.batting



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/total_averages")
def column ():    
    
    records = db.session.query(batting.yearid, batting.h, batting.ab).filter(batting.yearid.between( "1974", "1982")).all()
    df = pd.DataFrame(records, columns=['yearid', 'h', 'ab'])
        
    avg_1974_to1982 = df["h"]/df["ab"]
    #The following list returns the average of every single player from 1974 to 1982 ()
    avg_1974_to1982 = [x for x in avg_1974_to1982 if str(x) != 'nan']

    
    return jsonify(list(avg_1974_to1982))

    
    
if __name__ == "__main__":
    app.run(debug=True)    
    

    
#############   
# results = db.session.query(batting.yearid, batting.h, batting.ab)
# df = pd.DataFrame(results, columns=['yearid', 'h', 'ab'])
# return jsonify (df.to_dict())
#############
   
    
        

#############  
#    results = db.session.query(batting.yearid, batting.h, batting.ab).all()
#    year =[r[0] for r in results]
#    h = [r[1] for r in results]
#    ab = [r[2] for r in results]
#############


#############
#    results_dict = {
#   "year": year,
#    "h": h, 
#    "ab": ab
#    }
#   return jsonify (results_dict)
#############



#############
#h_ab =  data["h"] /  data["ab"]
#years = data.yearid
#return jsonify (list (h_ab[:10]))
#############
    
    

#############
# years_1974_to_1982 = df [(df [ 'yearid'] >=1974) & (df [ 'yearid'] <=1982) ]
# years_1974_to_1982_avg = years_1974_to_1982 ['h'] / years_1974_to_1982 ['ab'] 
#############




