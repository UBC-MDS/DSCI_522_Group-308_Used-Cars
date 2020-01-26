# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-25

'''The script loads previously trained model and performs validation on test data. It then
stores sample excerpt in data folder

Usage: test_model.py
'''

import numpy as np
import pandas as pd
import altair as alt
import altair as alt
from sklearn import tree
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC, SVR, LinearSVC
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import KFold
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import VotingClassifier, AdaBoostClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import datasets
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pickle
import os
import sys

MODEL_DUMP_PATH = 'model.pic'
TEST_EXCERPT_PATH = '../data/test_results_sample.csv'

if (not os.path.isfile(MODEL_DUMP_PATH)):
    print('ERROR - No model file. Run train_model.py first')
    sys.exit()

# Read the model from Pickle dump
print("Loading model...")
model = pickle.load(open(MODEL_DUMP_PATH, 'rb'))

# Read master train data
print("Loading test data...")
test_data = pd.read_csv('../data/vehicles_test.csv').dropna()
test_data = test_data[test_data.price != 0]
test_data = test_data[test_data.odometer != 0]

# Prepare the test data
y_test = test_data['price']
X_test = test_data[['year',
                    'odometer',
                    'manufacturer',
                    'transmission',
                    'fuel',
                    'paint_color',
                    'cylinders',
                    'drive',
                    'size',
                    'state',
                    'condition',
                    'title_status']]

# Run the test
print("Performing model predictions...")
test_score = model.score(X_test, y_test)
y_pred = model.predict(X_test)

# Report results to stdout
print()
print("Results:")
print("Test Observations:", len(y_test))
print("Average Test Price:", np.mean(y_test))
print("Accuracy:", test_score)
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("MAE", mean_absolute_error(y_test, y_pred))

# Generate except / sample for the report and store it in data folder
print()
print("Generating excerpt for report...")
sample_results = pd.concat([X_test.reset_index(drop = True),
                           pd.DataFrame(y_test).reset_index(drop = True),
                           pd.DataFrame(np.round(y_pred, 2), columns = ['prediction'])], axis = 1)
sample_results = sample_results[['year', 'odometer', 'manufacturer', 'condition', 'title_status', 'price', 'prediction']]
sample_results['abs_error'] = np.abs(sample_results['price'] - sample_results['prediction'])
sample_results['abs_error_pct'] = np.round(np.abs(100 * sample_results['abs_error'] / sample_results['price']), 2)
sample_results.sample(10).to_csv(TEST_EXCERPT_PATH)

print("DONE!")