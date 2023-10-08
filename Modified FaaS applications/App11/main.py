import time
init_st = time.time() * 1000
import os
import pickle
import gzip
import pandas as pd
import numpy as np
from sklearn import naive_bayes
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer


import gzip
import pickle

CLASSES = {
    0: "negative",
    4: "positive"
}

MODEL_FILE = 'model.dat.gz'
with gzip.open(MODEL_FILE, 'rb') as f:
    MODEL = pickle.load(f, encoding='bytes')


init_ed = time.time() * 1000


def lambda_handler(request):
    """
        Validate parameters and call the recommendation engine
        @event: API Gateway's POST body;
        @context: LambdaContext instance;
    """
    fun_st = time.time() * 1000
    # input validation
    # assert event, "AWS Lambda event parameter not provided"
    # text = event.get("text")  # query text
    # assert isinstance(text, basestring)
    text = "This function is awesome"
    # text = json.loads(event)["test"]

    # call predicting function
    print(predict(text))
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)




def predict(text):
    """
        Predict the sentiment of a string
        @text: string - the string to be analyzed
    """
    
    x_vector = MODEL.vectorizer.transform([text])
    
    y_predicted = MODEL.predict(x_vector)

    return CLASSES.get(y_predicted[0])

# print(lambda_handler(json.dumps({"test":"This function is awesome"})))
# print(lambda_handler("",""))


