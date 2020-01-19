# DSCI_522_Group-308_Used-Cars

Team members: Andrés Pitta, Braden Tam, Serhiy Pokrovskyy

# Project proposal 

## The Data
In this project, we will be conducting an analysis on the "Used Cars Dataset" from [Kaggle.com](https://www.kaggle.com/austinreese/craigslist-carstrucks-data). This dataset consists of Craigslist postings in the US that
contains the price of the listed vehicle and various features such as year, manufacturer, model, listed condition and odometer of the vehicle along with 9 other potential features that determine price. 

## Research Question
We will develop a model to answer the predictive question:   
**What features are most important in predicting the market price of a used car?**  
  
Our subquestion will be:  
**What is the predicted market price given a set of features of a car?**

## Analysis Plan of Action
The full dataset is roughly 1.4 GB in size so we will be taking a sample to improve the time and efficiency of our initial stages of the model building. We will be splitting the data to appropriate training, validation, and test sets in order to prevent biassing the results before conducting any analysis. Since we have a lot of data (~500 000 examples), we can afford to perform a more liberal split such as a 90/10 split to obtain a more accurate model. 

We will be fitting various supervised machine learning regression models such as random forest, XGBoost, support vector machine, etc. We will tune hyperparameters and evaluate model performance using cross-validation. Once we believe we've developed a suitable model, we will perform final predictions on the test set. 

## Exploratory Data Analysis
We will perform an [EDA](https://github.com/UBC-MDS/DSCI_522_Group-308_Used-Cars/blob/master/eda/EDA.ipynb) to get an overview of basic summary statistics, if there exists any outliers or eroneous data points, determining correlations between variables, if there exists multicollinearity in the data, and identifying which features we think will be most important. This EDA will help us understand the data and extract insights that will guide us further in our analysis. 

- A figure for a pearson's correlation matrix may be handy in determining if variables are redundant and may suggest variable importance.   
- A table for frequency of features will help determine where there are imbalances within the data which can be crucial to the interpretations of our results.   

## Communication of Results
For our final results, we will be creating a jupyter notebook that will contain an overview of our model including specifications and justifications. A table of the top predictors with a measure of importance will be presented as well as a table for predicted values and observed values. 
