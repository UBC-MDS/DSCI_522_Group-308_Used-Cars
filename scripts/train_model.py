# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-25

'''The script loads training data, performs [manual] feature selection and
fits a set of models. Script outputs train / test accuracies for different models
and dumps the best performing model to later be used by test_model.py

Usage: train_model.py
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
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

MODEL_DUMP_PATH = 'model222.pic'
TRAIN_DATA_PATH = '../data/vehicles_train.csv'

# Read master train data
print("Loading train data...")
train_data = pd.read_csv(TRAIN_DATA_PATH).dropna()
train_data = train_data[train_data.price != 0]
train_data = train_data[train_data.odometer != 0]

# Train / validation split
X_train, X_test, y_train, y_test = train_test_split(train_data[['year',
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
                                                                'title_status']],
                                                    train_data['price'],
                                                    test_size = 0.2,
                                                    random_state = 522)

# Define GridSearchCV pipeline with multiple models and param grids
grid_models = {
    'LinearRegression': GridSearchCV(LinearRegression(n_jobs=-1),
                                     n_jobs=-1,  # verbose=10,
                                     param_grid={'fit_intercept': [True]}),
    'SVR': GridSearchCV(SVR(),
                        n_jobs=-1,
                        verbose=10,
                        cv=2,
                        param_grid={'kernel': ['rbf'],
                                    'gamma': [0.12, 0.13, 0.14],
                                    'C': [5750, 6000, 6250]}),
    'KNeighborsRegressor': GridSearchCV(KNeighborsRegressor(n_jobs=-1),
                                        n_jobs=-1, verbose=10,
                                        param_grid={'n_neighbors': [100]}),
    'RandomForestRegressor': GridSearchCV(RandomForestRegressor(n_jobs=-1),
                                          n_jobs=-1, verbose=10,
                                          param_grid={'n_estimators': [100, 500]}),
    'XGBRegressor': GridSearchCV(XGBRegressor(n_jobs=-1),
                                 n_jobs=-1, verbose=10,
                                 param_grid={'n_estimators': [500, 1000]}),
    'LGBMRegressor': GridSearchCV(LGBMRegressor(n_jobs=-1),
                                  n_jobs=-1, verbose=10,
                                  param_grid={'n_estimators': [100, 500]}),
    'SGDRegressor': GridSearchCV(linear_model.SGDRegressor(),
                                 n_jobs=-1, verbose=10,
                                 param_grid={'loss': ['squared_loss', 'huber',
                                                      'epsilon_insensitive',
                                                      'squared_epsilon_insensitive'],
                                             'learning_rate': ['constant', 'optimal',
                                                               'invscaling', 'adaptive'],
                                             'alpha': [0.01, 0.1, 1, 10]
                                             })
}

# Transformation pipeline
num_transform = Pipeline(steps=[('scaler', StandardScaler())])
cat_transform = Pipeline(steps=[('ohe', OneHotEncoder())])
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
results = pd.DataFrame(columns=['Train Score', 'Test Score', 'Best Params', 'Model'])
pred_df = pd.DataFrame(columns=['Actual', 'Predicted', 'Classifier'])
for name, grid_model in grid_models.items():
    print(f"Fitting {name}...")

    # Define and fit
    classifier_ppl = Pipeline(steps=[('transformer', col_transform),
                                     ('classifier', grid_model)])
    classifier_ppl.fit(X_train, y_train)

    # Save summary
    print(f"Calculating accuracy for {name}...")
    results.loc[name] = [classifier_ppl.score(X_train, y_train),
                         classifier_ppl.score(X_test, y_test),
                         grid_model.best_params_,
                         classifier_ppl]

print()
print("Done training. Results:")
results.sort_values(by = ['Test Score'], ascending=False, inplace = True)
print(results.drop(['Model', 'Best Params'], axis = 1))
print()

best_model = results.iloc[0, 3]
print(f"Dumping {best_model.steps[1][1].estimator.__class__.__name__} model...")
pickle.dump(best_model, open(MODEL_DUMP_PATH, 'wb'))

print("DONE!")