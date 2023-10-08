from sklearn.datasets import fetch_california_housing
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
# from sklearn.externals import joblib
import joblib
import time

RANDOM_STATE = 42


dataset = fetch_california_housing()
print(dataset.DESCR)
dataset_df = pd.DataFrame(data=dataset.data, columns=dataset.feature_names)
dataset_df.info()
X_data, y_data = dataset.data, dataset.target
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=RANDOM_STATE)
print('Train data shape:', X_data.shape)
print('Test data shape:', X_test.shape)

def create_model():
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('selector', SelectKBest(score_func=f_regression, k=8)),
        ('svr', SVR(C=10, epsilon=0.1, gamma=1.0, kernel='rbf'))
    ])
    return model

# model = create_model()
# model.fit(X_train, y_train)
# y_pred_test = model.predict(X_test)
# print(mean_squared_error(y_test, y_pred_test))

model = create_model()
model.fit(X_data, y_data)
model_id = str(time.time()) 
model_name = 'model_' + model_id + '.joblib'
joblib.dump(model, model_name, compress=False)
print(model_name, 'saved.')