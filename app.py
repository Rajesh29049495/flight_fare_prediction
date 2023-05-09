from flask import Flask, request, jsonify, url_for, render_template
from ffp.predictor import ModelResolver
from ffp.exception import ffpException
from ffp.logger import logging
from ffp.entity import config_entity
from ffp.pipeline.training_pipeline import start_training_pipeline
from ffp.pipeline.batch_prediction import start_batch_prediction
from ffp import utils
import os,sys
import pandas as pd
import numpy as np
import datetime as dt
import pickle

app = Flask(__name__)

logging.info(f"Loading latest model from saved_models")
latest_dir = ModelResolver().get_latest_dir_path()

model_path= os.path.join(latest_dir,"model",config_entity.MODEL_FILE_NAME)
flight_model = utils.load_object(file_path=model_path)

logging.info(f"Loading Latest trasnformers from saved_models folder!!")

Airline_path = os.path.join(latest_dir,"transformer",config_entity.Airline_TRANSFORMER_OBJECT_FILE_NAME)
Source_Destination_path = os.path.join(latest_dir,"transformer",config_entity.Source_Destination_TRANSFORMER_OBJECT_FILE_NAME)
Total_Stops_path = os.path.join(latest_dir,"transformer",config_entity.Total_Stops_TRANSFORMER_OBJECT_FILE_NAME)
Additional_Info_path = os.path.join(latest_dir,"transformer",config_entity.Additional_Info_TRANSFORMER_OBJECT_FILE_NAME)
#reset_cols_path = os.path.join(latest_dir,"transformer",config_entity.reset_cols_TRANSFORMER_OBJECT_FILE_NAME)


Airline_transformer = utils.load_object(Airline_path)
Source_Destination_transformer = utils.load_object(Source_Destination_path)
Total_Stops_transformer = utils.load_object(Total_Stops_path)
Additional_Info_transformer = utils.load_object(Additional_Info_path)
#reset_cols_transformer = utils.load_object(reset_cols_path)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods= ['POST'])
def predict_api():
    data = [x for x in request.form.values()]                          ##extract all values from teh submitted forma and stores them in a list called "data"
    depart_time = data[0].split('T')[1]                                ##this extract time of departure from first element of the 'data' list, teh in ISO format{{example, the ISO format for May 9th, 2023 at 3:30 pm would be: "2023-05-09T15:30"}}, so the 'split' method is used to separate the date and time, and them the '[1]' index to extract only teh time
    result = dt.datetime.strptime(data[1], '%H:%M')-dt.datetime.strptime(depart_time,'%H:%M')     ##this calculates teh difference between teh scheduled arrival time and teh departure time. it first converts teh scheduled arrival time (which si teh second element of teh 'data' list) and teh departure time(which was extractd previously) to 'datetime' objects using teh 'strptime' method, and then subtracts them. the result is a 'timedelta' object.
    print(result.seconds/60)                                           ##the line prints the duration of the flight in minutes. teh 'seconds' attribute of teh 'timedelta' object is used to get the duration in seconds, which i then divided by 60 to get the duration in minutes.

    if dt.datetime.strptime(depart_time,'%H:%M')==dt.datetime.strptime(data[1], '%H:%M'):    ##checks, if departre time an darrival time same then it sets duration hours to 24 hours but if not then from teh diference is converted into hours and minutes
        duration_h =24
        duration_min = 0
    else:
        duration_h = (result.seconds/60)//60                    ##double forward slash calculate the integer number of hours 
        duration_min = (result.seconds/60)%60                   ##the modulus operatoru '%' calculaytes the remaining minutes
    print(duration_h, duration_min)

    filtered_data = []

    filetered_data.append(data[0].split('T')[0].split('-')[2])   ##departure 'date'
    filetered_data.append(data[0].split('T')[0].split('-')[1])   ##departure 'month'
    filetered_data.append(data[0].split('T')[1].split('-')[0])   ##'Dep_Time_hour'
    filetered_data.append(data[0].split('T')[1].split('-')[1])   ##'Dep_Time_min'
    filtered_data.append(data[1].split(':')[0])                  ##'Arrival_Time_hour'
    filtered_data.append(data[1].split(':')[1])                  ##'Arrival_Time_min'
    filtered_data.append(duration_h)                             ##'Duration hour'
    filtered_data.append(duration_min)                           ##'Duration min'
    filtered_data.append(data[2])                                ##'Airline'
    filtered_data.append(data[3])                                ##'Source'
    filtered_data.append(data[4])                                ##'Destination'
    filtered_data.append(data[5])                                ##'Total_Stops'
    filtered_data.append(data[6])                                ##'Additional_Info'
    print(filtered_data)

    filtered_data[8] = int((pd.Series(filtered_data[8]).map(Airline_transformer)).values)                  ##to apply map() function on list 'filtered_data' elements, we need to convert those elements into Pandas Series using 'pd.Series()', as 'map()' function in panadas is a method of the Series object, not a built-in function.
    filtered_data[9] = int((pd.Series(filtered_data[9]).map(Source_Destination_transformer)).values)       ##here we have replaced the list 'filtered_data' elemets at 8,9,10,11,12 index position with their mapped version present in the dictionaries i have imported from config_entity using utils
    filtered_data[10] = int((pd.Series(filtered_data[10]).map(Source_Destination_transformer)).values)     ##suppose a element in the list is "abc" then pd.Series("abc") will form a series with one element "0    abc" then mpping it "pd.Series("abc").map({"abc":2})" will give a series with one element "0    2", now extract this element '2' using "(pd.Series("abc").map({"abc":2})).values" and converting it into integer form using "int((pd.Series("abc").map({"abc":2})).values)"
    filtered_data[11] = int((pd.Series(filtered_data[11]).map(Total_Stops_transformer)).values)            ##in above mentoned way will map elements in the list
    filtered_data[12] = int((pd.Series(filtered_data[12]).map(Additional_Info_transformer)).values)

    print(filtered_data)
    
    filtered_data = [int(x) for x in filtered_data]            ##converting remaining values in the list into integer
    final_input= np.array(filtered_data).reshape(1,-1)         ##l = [0,1,2],,,np.array(l) will create 1D NumPy array: array(['0','1','2']), then 'reshape(1,-1)' is used to convert the 1D array into a 2D array with one row and an unknon number of columns: array([['0','1','2']]), thsi 2D array can eb used as input to machine learning models that expect a 2D array as input
    print(final_input)

    output = flight_model.predict(final_input)[0]
    print(output)

    return render_template('home.html', output_text="The Price of the fight is {}.".format(round(output,2)))

if __name__=="__main__":
    try:
        #app.run(debug=True)                ##in some cases, depending on our operating system an dnetwork configuration, 'debug = True' may prevent external clienets from connecting to teh server , in which case using 'host="0.0.0.0" instead may resolve the issue.
        app.run(host="0.0.0.0")
        #app.run(host="0.0.0.0", port=8000)

    except Exception as e:
       raise ffpException(e, sys)