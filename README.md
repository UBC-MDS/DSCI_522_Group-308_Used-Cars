
# Used Cars Price Prediction

DSCI-522 - Group 308 Authors: Andrés Pitta, Braden Tam, Serhiy
Pokrovskyy

## About

In this project we attempt to build a regression model which can predict
the price of used cars based on numerous features of the car. We tested
the following models: support vector regression, stochastic gradient
descent regression, linear regression, K-nearest neighbour regression,
and random forest regression. data set is not linearly separable, more
clustered. We found that support vector regression had the best results,
having an ![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score
of 0.843 on the training set,
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.772
on the validation set and
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.739
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
dependencies listed below and follow these instructions:

Before starting, if you want to reset all the outputs, run the following
command at the command line/terminal:

    make clean

**Warning** The dataset’s size is 1.35GB. In order to replicate a quick
version of the model with 1% of the data (see makefile documentation to
change train size), run the following command at the command
line/terminal:

    make quick

If you want to run the model with all the data run:

    make all

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

## Notes

Please be advised that in order to reproduce the analysis, the
`scripts/download.py` script will download approximately 1.4GB original
data file. Also, training the model with `scripts/train_model.py` may
take several hours. You may consider using command line arguments to
train on a configurable subset of training data (which may affect the
trained model) Please see consult usage data on each script for further
details and options.

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
