import time
init_st = time.time() * 1000
import pandas as pd
import numpy as np


from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import pickle
import random
import logging
import boto3
# import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
init_ed = time.time() * 1000

def predict_with_model(event):
    
    input_for_prediction = \
        pd.DataFrame({
            'fixed acidity': [event['fixed acidity']],
            'volatile acidity': [event['volatile acidity']],
            'citric acid': [event['citric acid']],
            'residual sugar': [event['residual sugar']],
            'chlorides': [event['chlorides']],
            'free sulfur dioxide': [event['free sulfur dioxide']],
            'total sulfur dioxide': [event['total sulfur dioxide']],
            'density': [event['density']],
            'pH': [event['pH']],
            'sulphates': [event['sulphates']],
            'alcohol': [event['alcohol']]})

    logger.info("Input data for prediction:")
    print("Input data for prediction:")
    logger.info(str(input_for_prediction))

    model_name = event['model name']
    # model_name = "model-1028"

    logger.info(" > Downloading model from S3 < ")

    temp_file_path = '/tmp/' + model_name
    # temp_file_path = model_name

    s3 = boto3.client('s3',aws_access_key_id="XXXX",                              aws_secret_access_key="XXXX",       region_name="us-west-1")
    s3.download_file("bucketname2", model_name, temp_file_path)

    logger.info(" > Loading model to memory < ")

    with open(temp_file_path, 'rb') as f:
        model = pickle.load(f)

    logger.info(" > Predicting wine quality < ")

    predicted_wine_grade = model.predict(input_for_prediction)
    # print(str(np.round(predicted_wine_grade, 1)))
    return str(np.round(predicted_wine_grade, 1))

def do_main(request):
    fun_st = time.time() * 1000
    event1 = {"model name": "model-1028",  
    "fixed acidity": "7.4",
    "volatile acidity": "0.70",
    "citric acid": "0.00",
    "residual sugar": "1.9",
    "chlorides": "0.076",
    "free sulfur dioxide": "11.0",
    "total sulfur dioxide": "34.0",
    "density": "0.9978",
    "pH": "3.51",
    "sulphates": "0.56",
    "alcohol": "9.4"
    }
    print(predict_with_model(event1))
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)





# do_main()