# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-25

'''The script loads previously trained model and performs validation on test data. It then
stores sample excerpt in data folder

Usage: test_model.py [--TEST_FILE_PATH=<TEST_FILE_PATH>] [--MODEL_DUMP_PATH=<MODEL_DUMP_PATH>] [--TEST_SIZE=<TEST_SIZE>]

Options:
--TEST_FILE_PATH=<TEST_FILE_PATH>    Test data file path [default: data/vehicles_test.csv]
--MODEL_DUMP_PATH=<MODEL_DUMP_PATH>  Path to load the model to test. [default: results/model.pic]
--TEST_SIZE=<TEST_SIZE>              Percentage of test set to use (from 0 to 1). [default: 1]
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
from docopt import docopt

opt = docopt(__doc__)

# Excerpt for the report path
TEST_EXCERPT_PATH = 'results/test_results_sample.csv'


def main(test_file_path, model_dump_path, test_size=1):
    """
    Main entry for script to load data and test the model.

    Arguments
    ---------
    test_file_path : str
        Path to test dataset.
    model_dump_path : str
        Path to dump the resulting model.
    test_size : float
        Percentage of test dataset to use, from 0 to 1 (Default = 1)
    """

    if (not os.path.isfile(test_file_path)):
        print('ERROR - No test file. Run scripts/wrangling.R first')
        sys.exit()

    if (not os.path.isfile(model_dump_path)):
        print('ERROR - No model file. Run scripts/train_model.py first')
        sys.exit()

    if test_size <= 0 or test_size > 1:
        print('ERROR - Invalid TEST_SIZE. Should be between 0 and 1')
        sys.exit()

    # Read the model from Pickle dump
    print("Loading model...")
    model = pickle.load(open(model_dump_path, 'rb'))

    # Read master test data
    print("Loading test data...")
    test_data = pd.read_csv(test_file_path).dropna()

    if test_size:
        test_data = test_data.sample(frac=test_size)
        print(f"Sampled test set to {len(test_data)} observations")
    else:
        print(f"Loaded full test set ({len(test_data)} observations)")

    # Prepare the test data
    X_test = test_data.drop(columns=['price'])
    y_test = test_data['price']

    # Run the test
    print("Running model predictions...")
    test_score = model.score(X_test, y_test)
    y_pred = model.predict(X_test)

    # Report results
    results_df = pd.DataFrame(columns=['Metric Value'])
    results_df.loc['R-Squared'] = [test_score]
    results_df.loc['RMSE'] = [np.sqrt(mean_squared_error(y_test, y_pred))]
    results_df.loc['MAE'] = [mean_absolute_error(y_test, y_pred)]
    results_df.to_csv('results/test_metrics.csv')
    print()
    print("Results:")
    print(results_df)

    # Generate except / sample for the report and store it in data folder
    print()
    print("Generating excerpt for report...")
    sample_results = pd.concat([X_test.reset_index(drop=True),
                                pd.DataFrame(y_test).reset_index(drop=True),
                                pd.DataFrame(np.round(y_pred, 2), columns=['prediction'])], axis=1)
    sample_results = sample_results[['year',
                                     'odometer',
                                     'manufacturer',
                                     'condition',
                                     'title_status',
                                     'price',
                                     'prediction']]
    sample_results['abs_error'] = np.abs(sample_results['price'] - sample_results['prediction'])
    sample_results['abs_error_pct'] = np.round(np.abs(100 * sample_results['abs_error'] / sample_results['price']), 2)
    sample_results.sample(10).to_csv(TEST_EXCERPT_PATH)

    print("DONE!")


if __name__ == "__main__":
    main(opt["--TEST_FILE_PATH"],
         opt["--MODEL_DUMP_PATH"],
         float(opt["--TEST_SIZE"]))
