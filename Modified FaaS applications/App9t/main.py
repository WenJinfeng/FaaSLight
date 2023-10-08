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
# s3_bucket = os.environ['s3_model_bucket']
# logger.info("Bucket for model is: " + str(s3_bucket))

def train_model(request):

    fun_st = time.time() * 1000
    # model_name_prefix = 'model-'
    dataset_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv'

    # Seeds to make the training repeatable
    data_split_seed = 2
    random_forest_seed = 2

    logger.info(" > Importing Data < ")
    print(" > Importing Data < ")

    data = pd.read_csv(
        dataset_url, header='infer', na_values='?', sep=';')

    # Uncomment to print data samples
    # print(str(data.head()))

    logger.info(" > Splitting in Training & Testing < ")

    np.random.seed(data_split_seed)

    data['split'] = np.random.randn(data.shape[0], 1)
    split = np.random.rand(len(data)) <= 0.90

    X_train = data[split].drop(['quality', 'split'], axis=1)
    X_test = data[~split].drop(['quality', 'split'], axis=1)

    y_train = data.quality[split]
    y_test = data.quality[~split].values

    logger.info(" > Training Random Forest Model < ")

    regressor = RandomForestRegressor(
            max_depth=None, n_estimators=30, random_state=random_forest_seed)

    regressor.fit(X_train, y_train)

    logger.info(" > Saving model to S3 < ")

    # model_name = model_name_prefix + str(random.randint(0, 100000))
    model_name = "model-1028"
    temp_file_path = '/tmp/' + model_name
    # temp_file_path = model_name

    with open(temp_file_path, 'wb') as f1:
        pickle.dump(regressor, f1)

    with open(temp_file_path, 'rb') as f2:
        model_data = f2.read()

    s3 = boto3.resource('s3',aws_access_key_id="XXXX",
                                aws_secret_access_key="XXXX",
                                region_name="us-west-1")
    s3_object = s3.Object("bucketname2", model_name)
    s3_object.put(Body=model_data)

    logger.info("Model saved with name: " + model_name)

    logger.info(" > Evaluating the Model < ")

    y_predicted = regressor.predict(X_test)

    logger.info(" Sample predictions on the test set < ")
    for i in range(20):
        logger.info("  label: " + str(y_test[i]) + " predicted: " + str(round(y_predicted[i], 2)))

    logger.info(" Mean Absolute Error on full test set: " + str(round(metrics.mean_absolute_error(y_test, y_predicted), 3)))
    # print(" Mean Absolute Error on full test set: " + str(round(metrics.mean_absolute_error(y_test, y_predicted), 3)))
    fun_ed = time.time() * 1000
    return ",InitStart:{},".format(init_st)+"InitEnd:{},".format(init_ed)+"functionStart:{},".format(fun_st)+"functionEnd:{},".format(fun_ed)


# train_model()

