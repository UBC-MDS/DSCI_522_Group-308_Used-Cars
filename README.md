
# Used Cars Price Prediction

DSCI-522 - Group 308 Authors: Andrés Pitta, Braden Tam, Serhiy
Pokrovskyy

## About

In this project we attempt to build a regression model which can predict
the price of used cars based on numerous features of the car. We tested
the following models: support vector regression, stochastic gradient
descent regression, linear regression, K-nearest neighbour regression,
and random forest regression. We found that support vector regression
had the best results, having an
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.877
on the training set, ![R^2](https://latex.codecogs.com/png.latex?R%5E2
"R^2") score of 0.832 on the validation set and
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.830
on the test set. The training and validation scores are computed from a
very small subset of the data while the test score used a much larger
subset. Given that the dataset was imbalanced, this led to poor
prediction of the classes that were quite sparse because the model was
not able to learn enough about those classes in order to give good
predictions on unseen data.

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

To replicate the analysis, clone this GitHub repository and follow these instructions:

1. Reset the repository and clean any prebuilt results:

```
make clean
```

2. Run the complete pipeline:

```
make all
```
    
**NOTE** The original dataset’s size is 1.35GB. Fitting the model may take many hours (seriously!) Thus, we provided a convenient method to replicate a quick version of the model with just a portion of the data:

1. Reset the repository without removing `data_vehicles.csv`:

```
  make partial_clean
  
```
2. Run the quick version of the pipeline:

```
  make quick TRAIN_SIZE=0.01
```    
    
You may choose other percentage value (0-to-1) For 1% (`TRAIN_SIZE=0.01`) expected runtime is 5 minutes. Keep in mind, that lower dataset size decreases accuracy.

To replicate the quick version of this analysis using docker run the following commands:

1. Reset the repository without removing `data_vehicles.csv`:

```
  make partial_clean
  
```
2. Run the quick version of the pipeline:

```
  make run_quick_from_docker
```    

**NOTE** You must have [Docker](https://www.docker.com/get-started) installed in order to run the above commands.

**NOTE** Running the pipeline will download a prebuilt Docker container for our project. Be advised, that the size of container is approximately 1.86 GB and the pipeline will then download additional 1.35 GB data file.

The dependencies of this pipeline are shown in the following diagram:

![Dendencies graph for the pipelin](Makefile.png)


## Dependencies

  - Python 3.7.3 and Python packages:
      - altair==3.2.0
      - selenium==3.141.0
      - docopt==0.6.2
      - pandas==0.24.2
      - numpy==1.16.4
      - statsmodel==0.10.0
      - plotly==4.3.0
      - plotly-orca==1.2.1
      - scikit-learn==0.20.4
  - R version 3.6.1 and R packages:
      - knitr==1.24
      - docopt==0.6.1
      - tidyverse==1.3.0
      - readr==1.3.1

## Notes

Please be advised that in order to reproduce the analysis, the
`scripts/download.py` script will download approximately 1.35GB original
data file. Also, training the full model with `scripts/train_model.py` may
take several hours. You may consider using command line arguments to
train on a configurable subset of training data (which may affect the
trained model) Please consult usage data for each script for further
details and command line arguments.

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
