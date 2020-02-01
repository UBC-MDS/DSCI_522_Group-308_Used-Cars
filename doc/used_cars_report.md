Predicting Used Car Prices
================
Andrés Pitta, Braden Tam, Serhiy Pokrovskyy </br>
2020/01/25 (updated: 2020-02-01)

# Summary

In this project we attempt to build a regression model which can predict
the price of used cars based on numerous features of the car. We tested
the following models: support vector regression, stochastic gradient
descent regression, linear regression, K-nearest neighbour regression,
and random forest regression. We found that support vector regression
had the best results, having an
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.885
on the training set, ![R^2](https://latex.codecogs.com/png.latex?R%5E2
"R^2") score of 0.758 on the validation set and
![R^2](https://latex.codecogs.com/png.latex?R%5E2 "R^2") score of 0.73
on the test set. Given that the dataset was imbalanced, this led to poor
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
performance. See the results below, sorted by validation score
(increasing):

<table class="table" style="margin-left: auto; margin-right: auto;">

<thead>

<tr>

<th style="text-align:left;">

Metric

</th>

<th style="text-align:right;">

Value

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

R-Squared

</td>

<td style="text-align:right;">

0.7298845

</td>

</tr>

<tr>

<td style="text-align:left;">

RMSE

</td>

<td style="text-align:right;">

5216.1417297

</td>

</tr>

<tr>

<td style="text-align:left;">

MAE

</td>

<td style="text-align:right;">

3555.7350475

</td>

</tr>

</tbody>

</table>

Since SVM shown the best results from the very beginning, we performed a
thorough adaptive grid search on more training data (200,000
observations, running for 4 hours) resulting in 81.4% accuracy on
validation data. Eventually we ran the model on the **test data**
containing more than 40,000 observations, which confirmed the model with
even better **accuracy of 81.6%**. The good sign was also that it did
not overfit greatly on train set, which was a good sign to perform
further testing.

<table class="table" style="margin-left: auto; margin-right: auto;">

<thead>

<tr>

<th style="text-align:left;">

Metric

</th>

<th style="text-align:right;">

Value

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:left;">

R-Squared

</td>

<td style="text-align:right;">

0.7298845

</td>

</tr>

<tr>

<td style="text-align:left;">

RMSE

</td>

<td style="text-align:right;">

5216.1417297

</td>

</tr>

<tr>

<td style="text-align:left;">

MAE

</td>

<td style="text-align:right;">

3555.7350475

</td>

</tr>

</tbody>

</table>

Here is a list of test examples showing the predicted used car prices:

<table class="table" style="margin-left: auto; margin-right: auto;">

<thead>

<tr>

<th style="text-align:right;">

year

</th>

<th style="text-align:right;">

odometer

</th>

<th style="text-align:left;">

manufacturer

</th>

<th style="text-align:left;">

condition

</th>

<th style="text-align:left;">

title\_status

</th>

<th style="text-align:right;">

price

</th>

<th style="text-align:right;">

prediction

</th>

<th style="text-align:right;">

abs\_error\_pct

</th>

</tr>

</thead>

<tbody>

<tr>

<td style="text-align:right;">

2016

</td>

<td style="text-align:right;">

113440

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

good

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

24990

</td>

<td style="text-align:right;">

13508.08

</td>

<td style="text-align:right;">

45.95

</td>

</tr>

<tr>

<td style="text-align:right;">

2000

</td>

<td style="text-align:right;">

125943

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

fair

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

4000

</td>

<td style="text-align:right;">

3056.89

</td>

<td style="text-align:right;">

23.58

</td>

</tr>

<tr>

<td style="text-align:right;">

2002

</td>

<td style="text-align:right;">

90802

</td>

<td style="text-align:left;">

lexus

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

4800

</td>

<td style="text-align:right;">

9819.96

</td>

<td style="text-align:right;">

104.58

</td>

</tr>

<tr>

<td style="text-align:right;">

2012

</td>

<td style="text-align:right;">

89950

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

6950

</td>

<td style="text-align:right;">

7986.51

</td>

<td style="text-align:right;">

14.91

</td>

</tr>

<tr>

<td style="text-align:right;">

2005

</td>

<td style="text-align:right;">

58364

</td>

<td style="text-align:left;">

pontiac

</td>

<td style="text-align:left;">

excellent

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

7200

</td>

<td style="text-align:right;">

10648.98

</td>

<td style="text-align:right;">

47.90

</td>

</tr>

<tr>

<td style="text-align:right;">

2017

</td>

<td style="text-align:right;">

45973

</td>

<td style="text-align:left;">

ford

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

13750

</td>

<td style="text-align:right;">

17056.06

</td>

<td style="text-align:right;">

24.04

</td>

</tr>

<tr>

<td style="text-align:right;">

2013

</td>

<td style="text-align:right;">

74517

</td>

<td style="text-align:left;">

toyota

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

26995

</td>

<td style="text-align:right;">

24875.58

</td>

<td style="text-align:right;">

7.85

</td>

</tr>

<tr>

<td style="text-align:right;">

2013

</td>

<td style="text-align:right;">

88230

</td>

<td style="text-align:left;">

hyundai

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

7998

</td>

<td style="text-align:right;">

6942.19

</td>

<td style="text-align:right;">

13.20

</td>

</tr>

<tr>

<td style="text-align:right;">

2003

</td>

<td style="text-align:right;">

157490

</td>

<td style="text-align:left;">

toyota

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

10450

</td>

<td style="text-align:right;">

4912.31

</td>

<td style="text-align:right;">

52.99

</td>

</tr>

<tr>

<td style="text-align:right;">

2018

</td>

<td style="text-align:right;">

27610

</td>

<td style="text-align:left;">

gmc

</td>

<td style="text-align:left;">

No value

</td>

<td style="text-align:left;">

clean

</td>

<td style="text-align:right;">

42950

</td>

<td style="text-align:right;">

27458.40

</td>

<td style="text-align:right;">

36.07

</td>

</tr>

</tbody>

</table>

# Further Directions

To further imrpove the accuracy of this model we can aleviate the
problem of imbalanced classes by grouping manufacturers by region
(American, Germnan, Italian, Japanese, British, etc.) and status type
(luxery vs economy).

Although we achieved a nice accuracy of 81.5%, we can now observe some
other metrics. Eg., having an RMSE almost twice higher than MAE suggests
that there is a good number of observations where the error is big (the
more RMSE differs from MAE, the higher is the variance) This is
something we may want to improve by finding features and clusters in
data space that introduce more variance in the predictions. Eg. the
model predicting clean car price may greatly differ from the model
predicting salvage (damage / total loss) car price. This comes from
getting deeper expertise in the area, and we will try to play with this
further more.

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
