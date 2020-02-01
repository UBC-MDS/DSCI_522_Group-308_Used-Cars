# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-25

'''The script loads training data, performs [manual] feature selection and
fits a set of models. Script outputs train / test accuracies for different models
and dumps the best performing model to be used by test_model.py.

IMPORTANT: By default, the script runs on 100% of training data and can take hours to complete.

Usage: train_model.py [--TRAIN_FILE_PATH=<TRAIN_FILE_PATH>] [--MODEL_DUMP_PATH=<MODEL_DUMP_PATH>] [--TRAIN_SIZE=<TRAIN_SIZE>] [--VERBOSE]

Options:
--TRAIN_FILE_PATH=<TRAIN_FILE_PATH>  Train data file path [default: data/vehicles_train.csv]
--MODEL_DUMP_PATH=<MODEL_DUMP_PATH>  Path to dump the resulting model. [default: results/model.pic]
--TRAIN_SIZE=<TRAIN_SIZE>            Percentage of train set to use (from 0 to 1). [default: 1]
--VERBOSE                            Turns on sklearn GridSearchCV verbose output
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
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pickle
import os
import sys
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from docopt import docopt

opt = docopt(__doc__)


def main(train_file_path, model_dump_path, train_size=1, verbose=False):
    """
    Main entry for script to load data and train the models.

    Arguments
    ---------
    train_file_path : str
        Path to training dataset.
    model_dump_path : str
        Path to dump the resulting model.
    train_size : float
        Percentage of train dataset to use, from 0 to 1 (Default = 1)
    """

    VERBOSE_GRID_SEARCH = 1 if verbose else 0

    if not os.path.isfile(train_file_path):
        print('ERROR - No train file. Run scripts/wrangling.R first')
        sys.exit()

    if train_size <= 0 or train_size > 1:
        print('ERROR - Invalid TRAIN_SIZE. Should be between 0 and 1')
        sys.exit()

    # Read master train data
    print("Loading train data...")
    train_data = pd.read_csv(train_file_path).dropna()

    if train_size:
        train_data = train_data.sample(frac=train_size)
        print(f"Sampled training set to {len(train_data)} observations")
    else:
        print(f"Loaded full training set ({len(train_data)} observations)")

    # Train / validation split
    print("Performing train-validation split...")
    X_train, X_valid, y_train, y_valid = train_test_split(train_data.drop(columns=['price']),
                                                          train_data['price'],
                                                          test_size=0.2,
                                                          random_state=522)

    print("Starging training...")

    # Define GridSearchCV pipeline with multiple models and param grids
    grid_models = {
        'LinearRegression': GridSearchCV(LinearRegression(n_jobs=-1),
                                         n_jobs=-1,
                                         verbose=VERBOSE_GRID_SEARCH,
                                         param_grid={'fit_intercept': [True]}),
        'SVR': GridSearchCV(SVR(),
                            n_jobs=-1,
                            verbose=VERBOSE_GRID_SEARCH,
                            cv=2,
                            param_grid={'kernel': ['rbf'],
                                        'gamma': [0.12, 0.13, 0.14],
                                        'C': [5750, 6000, 6250]}),
        'KNeighborsRegressor': GridSearchCV(KNeighborsRegressor(n_jobs=-1),
                                            n_jobs=-1,
                                            verbose=VERBOSE_GRID_SEARCH,
                                            param_grid={'n_neighbors': [100]}),
        'RandomForestRegressor': GridSearchCV(RandomForestRegressor(n_jobs=-1),
                                              n_jobs=-1,
                                              verbose=VERBOSE_GRID_SEARCH,
                                              param_grid={'n_estimators': [100, 500]}),
        'XGBRegressor': GridSearchCV(XGBRegressor(n_jobs=-1),
                                     n_jobs=-1,
                                     verbose=VERBOSE_GRID_SEARCH,
                                     param_grid={'n_estimators': [500, 1000]}),
        'LGBMRegressor': GridSearchCV(LGBMRegressor(n_jobs=-1),
                                      n_jobs=-1,
                                      verbose=VERBOSE_GRID_SEARCH,
                                      param_grid={'n_estimators': [100, 500]}),
    }

    # Transformation pipeline
    num_transform = Pipeline(steps=[('scaler', StandardScaler())])
    cat_transform = Pipeline(steps=[('ohe', OneHotEncoder(handle_unknown='ignore'))])
    col_transform = ColumnTransformer(transformers=[
        ('num', num_transform, ['year', 'odometer']),
        ('cat', cat_transform, ['manufacturer',
                                'transmission',
                                'fuel',
                                'paint_color',
                                'cylinders',
                                'drive',
                                'size',
                                'state',
                                'condition',
                                'title_status'
                                ])
    ])

    # Test each model
    results = pd.DataFrame(columns=['Train Score', 'Validation Score', 'Best Params', 'Model'])
    for name, grid_model in grid_models.items():
        print("-------------------------------------------------------------------------")
        print(f"Fitting {name}...")

        # Define and fit
        classifier_ppl = Pipeline(steps=[('transformer', col_transform),
                                         ('classifier', grid_model)])
        classifier_ppl.fit(X_train, y_train)

        # Save summary
        print(f"Calculating accuracy for {name}...")
        results.loc[name] = [classifier_ppl.score(X_train, y_train),
                             classifier_ppl.score(X_valid, y_valid),
                             grid_model.best_params_,
                             classifier_ppl]

    print("-------------------------------------------------------------------------")
    print()
    print("Done training. Results:")
    print()
    results.sort_values(by=['Validation Score'], ascending=False, inplace=True)
    print(results.drop(['Model', 'Best Params'], axis=1))
    print()

    # Dump training results to CSV for the report
    results.drop(['Model', 'Best Params'], axis=1).to_csv('results/train_metrics.csv')

    best_model = results.iloc[0, 3]
    print(f"Dumping {best_model.steps[1][1].estimator.__class__.__name__} model to {model_dump_path}...")
    pickle.dump(best_model, open(model_dump_path, 'wb'))

    print("DONE!")


if __name__ == "__main__":
    main(opt["--TRAIN_FILE_PATH"],
         opt["--MODEL_DUMP_PATH"],
         float(opt["--TRAIN_SIZE"]),
         opt["--VERBOSE"])
