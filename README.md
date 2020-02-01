
# DSCI\_522\_Group-308\_Used-Cars

authors: Andrés Pitta, Braden Tam, Serhiy Pokrovskyy

## About

In this project we attempt to build a regression model which can predict
the price of used cars based on numerous features of the car. We tested
the following models: support vector regression, stochastic gradient
descent regression, linear regression, K-nearest neighbour regression,
and random forest regression. data set is not linearly separable, more
clustered. We found that support vector regression had the best results,
having an ![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score
of 0.84 on the training set and an
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.814
on the test set. Given that the dataset was imbalanced, this led to poor
prediction of the classes that were quite sparse.

The data set used in this project is Used Cars Dataset created by Austin
Reese. It was collected from Kaggle.com (Reese 2020) and can be found
[here](https://www.kaggle.com/austinreese/craigslist-carstrucks-data).
This data consists of used car listings in the US scraped from
Craigslist that contains information such as listed price, manufacturer,
model, listed condition, fuel type, odometer, type of car, and which
state it’s being sold in.

## Report

The final report can be found
[here](https://github.com/UBC-MDS/DSCI_522_Group-308_Used-Cars/blob/master/doc/used_cars_report.md).

## Usage

To replicate the analysis, clone this GitHub repository, install the
dependencies listed below, and run the following commands at the command
line/terminal from the root directory of this project:

    # download data
    python scripts/download.py --DATA_FILE_PATH=../data/vehicles.csv --DATA_FILE_URL=http://mds.dev.synnergia.com/uploads/vehicles.csv --DATA_FILE_HASH=06e7bd341eebef8e77b088d2d3c54585
    
    # data wrangling
    Rscript scripts/wrangling.R --DATA_FILE_PATH=../data/vehicles.csv --TRAIN_FILE_PATH=../data/vehicles_train.csv --TEST_FILE_PATH=../data/vehicles_test.csv --TARGET=price --REMOVE_OUTLIERS=YES --TRAIN_SIZE= 0.9
    
    # EDA
    python scripts/eda.py --DATA_FILE_PATH=../data/vehicles_train.csv --EDA_FILE_PATH=../results/figures/
    
    # Model fitting and testing
    python scripts/train_model.py
    python scripts/test_model.py
    
    # Report
    Rscript -e "library(knitr); knit('doc/used_cars_report.Rmd')"

## Dependencies

  - Python 3.7.3 and Python packages:
      - altair==3.2.0
      - selenium==3.141.0
      - docopt==0.6.2
      - pandas==0.24.2
      - numpy==1.16.4
      - statsmodel==0.10.0
      - plotly==4.3.0
      - scikit-learn==0.20.4
  - R version 3.6.1 and R packages:
      - knitr==1.24
      - docopt==0.6.1
      - tidyverse==1.3.0
      - readr==1.3.1

## License

The Used Cars Prediction materials here are licensed under the Creative
Commons Attribution 2.5 Canada License (CC BY 2.5 CA). If
re-using/re-mixing please provide attribution and link to this webpage.

# References

<div id="refs" class="references">

<div id="ref-reese_2020">

Reese, Austin. 2020. “Used Cars Dataset.” *Kaggle*.
<https://www.kaggle.com/austinreese/craigslist-carstrucks-data>.

</div>

</div>
