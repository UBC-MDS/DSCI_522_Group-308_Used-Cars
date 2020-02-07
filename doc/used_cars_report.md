Predicting Used Car Prices
================
Andrés Pitta, Braden Tam, Serhiy Pokrovskyy </br>
2020/01/25 (updated: 2020-02-07)

# Summary

In this project we attempt to build a regression model which can predict
the price of used cars based on numerous features of the car. We tested
the following models: support vector regression, stochastic gradient
descent regression, linear regression, K-nearest neighbour regression,
and random forest regression. We found that support vector regression
had the best results, having an
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.833
on the training set, ![R^2](https://latex.codecogs.com/png.latex?R%5E2
"R^2") score of 0.73 on the validation set and
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.816
on the test set. The training and validation scores are computed from a
very small subset of the data while the test score used a much larger
subset. Given that the dataset was imbalanced, this led to poor
prediction of the classes that were quite sparse because the model was
not able to learn enough about those classes in order to give good
predictions on unseen data.

# Introduction

Websites such as Craigslist, Kijiji, and eBay have tons of users that
create a wide array of used good markets. Typically people looking to
save some money use these website to purchase second hand items. The
problem with these websites is that the user determines the price of
their used good. This can either be a good or bad thing, depending on
whether or not the user is trying to scam the buyer or give the buyer a
good deal. For the average individual who is not familiar with prices of
the used market, it is especially difficult to gauge what the price of a
used good should be. Being able to predict used car prices based on data
on a whole market will gives users the ability to evaluate whether a
used car listing is consistent with the market so that they know they
are not getting ripped off.

# Methods

## Data

The data set used in this project is Used Cars Dataset created by Austin
Reese. It was collected from Kaggle.com (Reese 2020) and can be found
[here](https://www.kaggle.com/austinreese/craigslist-carstrucks-data).
This data consists of used car listings in the US scraped from
Craigslist that contains information such as listed price, manufacturer,
model, listed condition, fuel type, odometer, type of car, and which
state it’s being sold in.

## Analysis

The R and Python programming languages (R Core Team 2019; Van Rossum and
Drake 2009) and the following R and Python packages were used to perform
the analysis: docopt (de Jonge 2018), knitr (Xie 2014), tidyverse
(Wickham et al. 2019), readr (Wickham, Hester, and Francois 2018) docopt
(Keleshev 2014), altair (VanderPlas et al. 2018), plotly (Inc. 2015),
selenium (SeleniumHQ 2020), pandas (McKinney 2010), numpy (Oliphant
2006), statsmodel (Seabold and Perktold 2010). scikit-learn (Buitinck et
al. 2013).

The code used to perform the analysis and create this report can be
found [here](https://github.com/UBC-MDS/DSCI_522_Group-308_Used-Cars)

As it was mentioned, our original data holds half a million observations
with a few dozen features, most categorical, so accurate feature
selection and model selection were extremely important. Especially
because model training took significant amount of computational
resources.

Since we could not efficiently use automated feature selection like RFE
or FFE (because of time / resources constraint), we had to perform
manual feature selection. As we had some intuition in the target area as
well as some practical experience, we were able to prune our feature
list to just 12 most important on our opinion:

  - 10 categorical features:
      - manufacturer (brand)
      - transmission type
      - fuel type
      - paint color
      - number of cylinders
      - drive type (AWD / FWD / RWD)
      - size
      - condition
      - title\_status
      - state
  - 2 continuous features:
      - year
      - odometer

The following plots are just a few examples of us visual representations
of what variables seem to be important in predicting used car prices.
The code used to generate these plots can be found
[here](https://github.com/UBC-MDS/DSCI_522_Group-308_Used-Cars/blob/master/scripts/eda.py).

![](../results/figures/manufacturer.png)
![](../results/figures/map_price.png)

<img src="../results/figures/manufacturer.png" width="80%" />

<img src="../results/figures/map_price.png" width="80%" />

<img src="../results/figures/corrplot.png" width="80%" />

For hyper-paramter tuning of each model we performed a
5-fold-cross-validated grid search involving a range of the most
important model-specific hyper-parameters. We chose to use 5-folds
because we have a lot of data to work with so this amount would provide
an optimal trade-off between computational time and finding the most
unbiased estimates of our models.

# Results & Discussion

Based on our EDA and assumptions, we picked a number of models to fit
our train data. Since training and validating took a lot of resources,
we performed it on a gradually increasing subsets of training data in
the hopes that we find an optimal amount of required data for maximal
performance. The metric used to evaluate our model is
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2"), which is a
value from 0 to 1 that gives the proportions of the variance in price
that is explained by our model. See the results below, sorted by
validation score:

<table class="table" style="margin-left: auto; margin-right: auto;">

<thead>

<tr>

<th style="text-align:left;">

Model

</th>

<th style="text-align:right;">

Train Score

</th>

<th style="text-align:right;">

Validation Score

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

SVR

</td>

<td style="text-align:right;">

0.8333795

</td>

<td style="text-align:right;">

0.7302227

</td>

</tr>

<tr>

<td style="text-align:left;">

LGBMRegressor

</td>

<td style="text-align:right;">

0.8841968

</td>

<td style="text-align:right;">

0.7245057

</td>

</tr>

<tr>

<td style="text-align:left;">

XGBRegressor

</td>

<td style="text-align:right;">

0.8583296

</td>

<td style="text-align:right;">

0.7158381

</td>

</tr>

<tr>

<td style="text-align:left;">

RandomForestRegressor

</td>

<td style="text-align:right;">

0.9603970

</td>

<td style="text-align:right;">

0.6977895

</td>

</tr>

<tr>

<td style="text-align:left;">

KNeighborsRegressor

</td>

<td style="text-align:right;">

0.5977437

</td>

<td style="text-align:right;">

0.5824930

</td>

</tr>

<tr>

<td style="text-align:left;">

LinearRegression

</td>

<td style="text-align:right;">

0.5941379

</td>

<td style="text-align:right;">

0.3793075

</td>

</tr>

</tbody>

</table>

Since SVM shown the best results from the very beginning, we performed a
thorough adaptive grid search on more training data (200,000
observations, running for 4 hours) to devise a more robust model.
Finally, we ran the model on the **test data** containing more than
40,000 observations, which confirmed the model with an
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") value of
**0.816**. The good sign was also that it did not overfit greatly on
train set, which was a good sign to perform further testing.

| Metric                                                   | Value    |
| -------------------------------------------------------- | -------- |
| ![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") | 0.815724 |
| RMSE                                                     | 4366.43  |
| MAE                                                      | 2691.71  |
| Average Price                                            | 13819.99 |

Here is a list of test examples showing the predicted used car prices:

<table class="table" style="margin-left: auto; margin-right: auto;">

<thead>

<tr>

<th style="text-align:right;">

Year

</th>

<th style="text-align:right;">

Odometer

</th>

<th style="text-align:left;">

Manufacturer

</th>

<th style="text-align:left;">

Condition

</th>

<th style="text-align:right;">

Price (USD)

</th>

<th style="text-align:right;">

Prediction

</th>

<th style="text-align:right;">

Absolute Error (%)

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:right;">

2014

</td>

<td style="text-align:right;">

70487

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

22990

</td>

<td style="text-align:right;">

19426.48

</td>

<td style="text-align:right;">

15.50

</td>

</tr>

<tr>

<td style="text-align:right;">

2013

</td>

<td style="text-align:right;">

175955

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:right;">

12995

</td>

<td style="text-align:right;">

8657.86

</td>

<td style="text-align:right;">

33.38

</td>

</tr>

<tr>

<td style="text-align:right;">

2008

</td>

<td style="text-align:right;">

162122

</td>

<td style="text-align:left;">

pontiac

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:right;">

2800

</td>

<td style="text-align:right;">

3005.86

</td>

<td style="text-align:right;">

7.35

</td>

</tr>

<tr>

<td style="text-align:right;">

2018

</td>

<td style="text-align:right;">

43466

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:right;">

22259

</td>

<td style="text-align:right;">

26031.71

</td>

<td style="text-align:right;">

16.95

</td>

</tr>

<tr>

<td style="text-align:right;">

2005

</td>

<td style="text-align:right;">

52349

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

15990

</td>

<td style="text-align:right;">

9532.39

</td>

<td style="text-align:right;">

40.39

</td>

</tr>

<tr>

<td style="text-align:right;">

2009

</td>

<td style="text-align:right;">

444206

</td>

<td style="text-align:left;">

dodge

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:right;">

1150

</td>

<td style="text-align:right;">

10612.54

</td>

<td style="text-align:right;">

822.83

</td>

</tr>

<tr>

<td style="text-align:right;">

2010

</td>

<td style="text-align:right;">

124925

</td>

<td style="text-align:left;">

audi

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

6995

</td>

<td style="text-align:right;">

4429.34

</td>

<td style="text-align:right;">

36.68

</td>

</tr>

<tr>

<td style="text-align:right;">

2002

</td>

<td style="text-align:right;">

59794

</td>

<td style="text-align:left;">

chrysler

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

4995

</td>

<td style="text-align:right;">

2581.31

</td>

<td style="text-align:right;">

48.32

</td>

</tr>

<tr>

<td style="text-align:right;">

2010

</td>

<td style="text-align:right;">

38103

</td>

<td style="text-align:left;">

toyota

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

15000

</td>

<td style="text-align:right;">

9689.95

</td>

<td style="text-align:right;">

35.40

</td>

</tr>

<tr>

<td style="text-align:right;">

2015

</td>

<td style="text-align:right;">

51000

</td>

<td style="text-align:left;">

chrysler

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:right;">

9950

</td>

<td style="text-align:right;">

10361.29

</td>

<td style="text-align:right;">

4.13

</td>

</tr>

</tbody>

</table>

# Further Directions

To further imrpove the ![R^2](https://latex.codecogs.com/png.latex?R%5E2
"R^2") of this model we can aleviate the problem of imbalanced classes
by grouping manufacturers by region (American, Germnan, Italian,
Japanese, British, etc.) and status type (luxery vs economy).

Although we achieved a solid
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") value of 0.816,
we can now observe some other metrics. Eg., having an RMSE almost twice
higher than MAE suggests that there is a good number of observations
where the error is big (the more RMSE differs from MAE, the higher is
the variance) This is something we may want to improve by finding
features and clusters in data space that introduce more variance in the
predictions. Eg. the model predicting clean car price may greatly differ
from the model predicting salvage (damage / total loss) car price. This
comes from getting deeper expertise in the area, and we will try to play
with this further more.

We may also want to use a different scoring function for our model - eg.
some custom implementation of MSE of relative error, since we have high
variance of price in the original dataset.

Lastly, due to time / resources limitations we only trained the model on
half the training data, so we should try to run it on all training data
and see how this changes our model (this would take approximately 16
hours). So far we have only seen improvements to the score as we
increased the sample size.

The ultimate end goal is to eventually create a command-line tool for
the end-user to interactively request vehicle details and output
expected price with a precision interval.

# References

<div id="refs" class="references">

<div id="ref-sklearn_api">

Buitinck, Lars, Gilles Louppe, Mathieu Blondel, Fabian Pedregosa,
Andreas Mueller, Olivier Grisel, Vlad Niculae, et al. 2013. “API Design
for Machine Learning Software: Experiences from the Scikit-Learn
Project.” In *ECML Pkdd Workshop: Languages for Data Mining and Machine
Learning*, 108–22.

</div>

<div id="ref-docopt">

de Jonge, Edwin. 2018. *Docopt: Command-Line Interface Specification
Language*. <https://CRAN.R-project.org/package=docopt>.

</div>

<div id="ref-plotly">

Inc., Plotly Technologies. 2015. “Collaborative Data Science.” Montreal,
QC: Plotly Technologies Inc. 2015. <https://plot.ly>.

</div>

<div id="ref-docoptpython">

Keleshev, Vladimir. 2014. *Docopt: Command-Line Interface Description
Language*. <https://github.com/docopt/docopt>.

</div>

<div id="ref-mckinney-proc-scipy-2010">

McKinney, Wes. 2010. “Data Structures for Statistical Computing in
Python.” In *Proceedings of the 9th Python in Science Conference*,
edited by Stéfan van der Walt and Jarrod Millman, 51–56.

</div>

<div id="ref-oliphant2006guide">

Oliphant, Travis E. 2006. *A Guide to Numpy*. Vol. 1. Trelgol Publishing
USA.

</div>

<div id="ref-R">

R Core Team. 2019. *R: A Language and Environment for Statistical
Computing*. Vienna, Austria: R Foundation for Statistical Computing.
<https://www.R-project.org/>.

</div>

<div id="ref-reese_2020">

Reese, Austin. 2020. “Used Cars Dataset.” *Kaggle*.
<https://www.kaggle.com/austinreese/craigslist-carstrucks-data>.

</div>

<div id="ref-seabold2010statsmodels">

Seabold, Skipper, and Josef Perktold. 2010. “Statsmodels: Econometric
and Statistical Modeling with Python.” In *9th Python in Science
Conference*.

</div>

<div id="ref-seleniumhq_2020">

SeleniumHQ. 2020. “SeleniumHQ/Selenium.” *GitHub*.
<https://github.com/SeleniumHQ/selenium>.

</div>

<div id="ref-Altair2018">

VanderPlas, Jacob, Brian Granger, Jeffrey Heer, Dominik Moritz, Kanit
Wongsuphasawat, Arvind Satyanarayan, Eitan Lees, Ilia Timofeev, Ben
Welsh, and Scott Sievert. 2018. “Altair: Interactive Statistical
Visualizations for Python.” *Journal of Open Source Software*, December.
The Open Journal. <https://doi.org/10.21105/joss.01057>.

</div>

<div id="ref-Python">

Van Rossum, Guido, and Fred L. Drake. 2009. *Python 3 Reference Manual*.
Scotts Valley, CA: CreateSpace.

</div>

<div id="ref-tidyverse">

Wickham, Hadley, Mara Averick, Jennifer Bryan, Winston Chang, Lucy
D’Agostino McGowan, Romain François, Garrett Grolemund, et al. 2019.
“Welcome to the tidyverse.” *Journal of Open Source Software* 4 (43):
1686. <https://doi.org/10.21105/joss.01686>.

</div>

<div id="ref-readr">

Wickham, Hadley, Jim Hester, and Romain Francois. 2018. *Readr: Read
Rectangular Text Data*. <https://CRAN.R-project.org/package=readr>.

</div>

<div id="ref-knitr">

Xie, Yihui. 2014. “Knitr: A Comprehensive Tool for Reproducible Research
in R.” In *Implementing Reproducible Computational Research*, edited by
Victoria Stodden, Friedrich Leisch, and Roger D. Peng. Chapman;
Hall/CRC. <http://www.crcpress.com/product/isbn/9781466561595>.

</div>

</div>
