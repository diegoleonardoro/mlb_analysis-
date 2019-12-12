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

# DATABASE_URL will contain the database connection string:
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres://iliraydnrlzapj:ba13fda65e251bf10b078f4afa008d625c25a69995c5ca69485cf45627378c5c@ec2-174-129-255-4.compute-1.amazonaws.com:5432/d28umiqbj9nbbb')

# Connects to the database using the app config
db = SQLAlchemy(app)

#reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(db.engine, reflect=True)
# Save references to each table
batting = Base.classes.batting



@app.route("/")
def home():

    all_records = db.session.query(batting.playerid, batting.yearid, batting.h, batting.ab).all()
    entire_df = pd.DataFrame(all_records, columns=['playerid','yearid', 'h', 'ab']) 

 #Create a new column with the average of every player, and calculate the std off that new column:
    
    entire_df["AVG"] = entire_df["h"] / entire_df["ab"] 

    total_years = np.arange (1871, 2019)
   #calculate all yeats averages: 

    all_years_avgs_ = []
    for year in total_years:
        x = entire_df [entire_df["yearid"] == str(year)]
        try:
            avg = sum (x["h"]) / sum (x["ab"])
        except ZeroDivisionError:
            continue
        all_years_avgs_.append (avg)

  

   # calculate std:
    std_per_year = []
    for year in total_years:
        x = entire_df[entire_df["yearid"]== str (year)]
        std = np.std (x["AVG"])
        std_per_year.append (std)

    


    # zscore = x - mean / std 
    mendo_avg = 0.21465968586387435
    mendo_zscores = {}
    mendo_zscores["year"] = []
    mendo_zscores["zscore"] = []
    for year,avg, std in zip(total_years, all_years_avgs_, std_per_year ):
        zscore = mendo_avg - avg / std
        mendo_zscores["year"].append (int (year))
        mendo_zscores["zscore"].append(float (zscore))
 
    

    return render_template("index.html",  response=mendo_zscores)





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
    mario_mendoza_avg = mario_mendoza["h"] /  mario_mendoza["ab"] 
    mario_mendoza_avg = mario_mendoza_avg.values.tolist()


    #query database to get all years:
    all_records = db.session.query(batting.playerid, batting.yearid, batting.h, batting.ab).all()
    entire_df = pd.DataFrame(all_records, columns=['playerid','yearid', 'h', 'ab']) 


    #Let's calculate the avg for every player every year from 1871 to 2018:
    entire_df["AVG"] = entire_df["h"] / entire_df["ab"]

   
# -------------- calculate the averages of every year:

    total_years = np.arange (1871, 2019)

    all_years_avgs_ = []  # this list contains the average of every single year from 1871 to 2019
    
    max_ =[]

    for year in total_years:
        x = entire_df [entire_df["yearid"] == str(year)]

        u= max (x["AVG"])
        year_ = x["yearid"].iloc[0]
        # max_.append (u + year_)

        # pprint (u)
        # pprint (year_)
        # pprint ("-"*100)

        try:
            avg = sum (x["h"]) / sum (x["ab"])
        except ZeroDivisionError:
            continue
        all_years_avgs_.append (avg)

   



    # samples_every_18_years is a list of lists containing the averages of each year. The list is divided by lists of 18 years.
    # samples_every_18_years is a list of 9 lists
    samples_every_18_years = [all_years_avgs_[i:i+18] for i in range(0, len(all_years_avgs_), 18)] 
    avgs_every_18_years = [sum(x)/len (x) for x in samples_every_18_years]



# -------------- Let's divide the dataframe every 18 years:
 
    years_every_18 = np.arange (1871, 2019, 18)
    entire_df ["yearid"] = entire_df ["yearid"].apply(pd.to_numeric)
    # the following three lines are gonna create the values that will go in the dropdow menu:
    labels_for_dropdow = ["1871 to 1889", "1890 to 1908","1909 to 1927","1928 to 1946","1947 to 1965","1966 to 1984","1985 to 2003","2004 to 2018"]
    year_bins = np.arange (1871,2019,18)
    year_bins_column = pd.cut(entire_df["yearid"], year_bins, labels =labels_for_dropdow)
    entire_df ["year_range"] = year_bins_column
    


    entire_df_divided_by_18_years =[] # this list contains dictionaries with the following values: ['playerid','yearid', 'h', 'ab']
    for year in years_every_18:
        x = entire_df [(entire_df ["yearid"]>=year) & (entire_df ["yearid"]< year + 18 )]
        x = x [x["AVG"]!=1.0]
        max_avg = max (x["AVG"])
        max_rows =  x[ x["AVG"]== max_avg]
        max_rows = max_rows.head(1) # this contains a data frame with just one record (the one that contains the max "AVG")
        
        entire_df_divided_by_18_years.apped(dict(max_rows)) # This is supposed to append all dictionaries to a list 
        


     return jsonify (entire_df_divided_by_18_years)
   
    
# --------------  #



 # -------------- Let's get the maximum and minimum batting average for every time frame of 18 years:
 
 #   max_avgs_every_18_years = []
 #   min_avgs_every_18_years = []
    
 #   for sample in samples_every_18_years:
 #       max_avg = '%.6f'% (max(sample))
 #       min_avg = '%.6f'% (min (sample))
 #       max_avgs_every_18_years.append (max_avg)
 #       min_avgs_every_18_years.append (min_avg)

 ##  pprint (max_avgs_every_18_years)
 # --------------  #



    
# -------------- Let's return only the values that match the maximim or minimum averages
 #   max_rows = []
 #   min_rows = []
 #   for max_, min_, data in zip (max_avgs_every_18_years, min_avgs_every_18_years, entire_df_divided_by_18_years):
 #       max_row = data [data["AVG"] == float (max_)]
 #       min_row = data [data["AVG"] == float (min_)]        
 #       max_rows.append (max_row)
 #       min_rows.append (min_row)
 # --------------  #




 # --------------  #
    
    mendoza_avg_vs_mlb = {"mendonza_average":mario_mendoza_avg, "average_by_year_74_to_82":average_by_year, "averages_every_18_years":avgs_every_18_years, "samples_every_18_years":samples_every_18_years}
    
    #return jsonify (entire_df_divided_by_18_years[0].to_dict())
    #return render_template("mendoza_averages.html",  response=mendoza_avg_vs_mlb)

    

    
            
                 
if __name__ == "__main__":
    app.run(debug=True, 
         host='0.0.0.0', 
         port=9000, 
         threaded=True)   

 




    




