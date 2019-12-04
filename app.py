import pandas as pd
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import numpy as np
from pprint import pprint


from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)


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


@app.route("/mendoza_averages")
def get_data ():    
    #query database to get years 1972 to 1983:
    records = db.session.query(batting.playerid, batting.yearid, batting.h, batting.ab).filter(batting.yearid.between( "1974", "1982")).all()
    df = pd.DataFrame(records, columns=['playerid','yearid', 'h', 'ab'])
    years_1974_to_1982 = np.arange (1972, 1983)
    
    average_by_year = []
    for year in years_1974_to_1982:
        x = df[df["yearid"] == str (year)]
        try:
            y = sum (x ["h"]) /sum ( x["ab"])
        except ZeroDivisionError:
            continue
        average_by_year.append(y)

    mario_mendoza = df [df["playerid"]=="mendoma01"]
    mario_mendoza_avg = mario_mendoza["h"] / mario_mendoza["ab"] 
    mario_mendoza_avg = mario_mendoza_avg.values.tolist()


    #query database to get all years:
    all_records = db.session.query(batting.playerid, batting.yearid, batting.h, batting.ab).all()
    entire_df = pd.DataFrame(all_records, columns=['playerid','yearid', 'h', 'ab'])   
    pprint(entire_df)

   
    #1871
    total_years = np.arange (1871, 2019)
    all_years_avgs_ = []
    for year in total_years:
        #print("current year: ",str(year))
        x = entire_df [entire_df["yearid"] == str(year)]
        #pprint(x)
        try:
            #print("calcing")
            #pprint(x["h"])
            avg = sum (x["h"]) / sum (x["ab"])
        except ZeroDivisionError:
            continue
        all_years_avgs_.append (avg)

    #return jsonify(all_years_avgs_)

    samples_every_18_years = [all_years_avgs_[i:i+18] for i in range(0, len(all_years_avgs_), 18)] 
    avgs_every_18_years = [sum(x)/len (x) for x in samples_every_18_years]

 # -------------- #





    #Create a new column with the average of every player, and calculate the std off that new column:
    
 #   entire_df["AVG"] = entire_df["h"] / entire_df["ab"] 

    
 #   std_per_year = []
 #   for year in total_years:
 #       x = entire_df[entire_df["yearid"]==year]
 #       std = np.std (x["AVG"])
 #       std_per_year.append (str (std))

    # zscore = x - mean / std 
 #   mendo_avg = 0.21465968586387435
 #   mendo_zscores = []
 #   for avg, std in zip(all_years_avgs_, std_per_year):
 #       zscore = mendo_avg - avg / std
 #       mendo_zscores.append (str (zscore))

    
    mendoza_avg_vs_mlb = {"mendonza_average":mario_mendoza_avg, "average_by_year_74_to_82":average_by_year, "averages_every_18_years":avgs_every_18_years, "samples_every_18_years":samples_every_18_years}
    
    #return jsonify (samples_every_18_years)
    return render_template("mendoza_averages.html",  response=mendoza_avg_vs_mlb)


    
            
                 
if __name__ == "__main__":
    app.run(debug=True, 
         host='0.0.0.0', 
         port=9000, 
         threaded=True)   

 




    




