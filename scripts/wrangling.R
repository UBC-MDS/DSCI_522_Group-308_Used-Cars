# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-24

"This script wrangles the data for ML purposes. It takes the following arguments: 
    the file were the root file is,
    the path where the test and train dataset is going to be saved, 
    the train/test set split in decimal numbers,
    and a boolean where TRUE = remove outliers and false do not remove.

Usage: wrangling.R [--DATA_FILE_PATH=<DATA_FILE_PATH>] [--TRAIN_FILE_PATH=<TRAIN_FILE_PATH>] [--TEST_FILE_PATH=<TEST_FILE_PATH>] [--TARGET=<TARGET>][--REMOVE_OUTLIERS=<REMOVE_OUTLIERS>] [--TRAIN_SIZE=<TRAIN_SIZE>]

Options:
--DATA_FILE_PATH=<DATA_FILE_PATH>  Path (including filename) to retrieve the csv file. [default: ../data/vehicles.csv]
--TRAIN_FILE_PATH=<TRAIN_FILE_PATH>  Path (including filename) to print the train portion as a csv file. [default: ../data/vehicles_train.csv]
--TEST_FILE_PATH=<TEST_FILE_PATH>  Path (including filename) to print the test portion as a csv file. [default: ../data/vehicles_test.csv]
--TARGET=<TARGET> Name of the response variable to use. [default: price]
--REMOVE_OUTLIERS=<REMOVE_OUTLIERS> Logical value that takes YES as value if the outliers should be remove, NO otherwise. [default: YES]
--TRAIN_SIZE=<TRAIN_SIZE> Decimal value for the train/test split. [default: 0.9] 
" -> doc

library(tidyverse, quietly = TRUE)
library(docopt, quietly = TRUE)
library(readr, quietly = TRUE)
library(stats, quietly = TRUE)
set.seed(1234)

opt <- docopt(doc)

main <- function(data_path, train_path, test_path, target, remove_outliers, train_size) {
  data <- load(data_path)
  list_traintest <- split_data(data, train_size)
  wrangled_train <- wrangling(list_traintest[[1]], target, remove_outliers)
  print_dataset(train_path, wrangled_train)
  print_dataset(test_path, list_traintest[[2]])
}

#' Loads the data from a provided path
#'
#' @param data_path path from where to load the data
#' @return the data
#' @examples
#' load('../data/vehicles.csv')
load <- function(data_path) {
  if (file.exists(data_path)) {
    return(readr::read_csv(data_path) %>% select(-c(description, county, url, region_url)))
  }
  else {
    print("The path does not exist")
  }
}


#' Data wrangling function. Fills all the NAs from the character variables with 'No value',
#' Removes the 99th-percentile from the target variable.
#'
#' @param data data to perform data wrangling
#' @param target response variable
#' @param remove_outliers TRUE if the user wants to remove values over the 99th percentile, FALSE if not.
#' @return the data
#' @examples
#' wrangling(vehicles, price, TRUE)
wrangling <- function(data, target, remove_outliers) {
  for (i in names(data)) {
    if (is.character(data[[i]])) {
      data[[i]] <- if_else(is.na(data[[i]]), "No value", data[[i]])
    }
  }

  if (remove_outliers == "YES") {
    data_filtered <- data[data[[target]] <= quantile(data[[target]], c(0.99)),]
    data_filtered <- data_filtered[data_filtered[[target]] > 10,]
    data_filtered <- data_filtered %>% filter(odometer > 0)
    data_filtered <- data_filtered %>% 
                      group_by(manufacturer) %>% 
                      mutate(freq = n()) %>% 
                      ungroup() %>% 
                      filter(freq > 100) %>%
                      select(-freq)

  } else {
    data_filtered <- data
  }
  return(data_filtered)
}

#' Splits the data given a train_size parameter
#'
#' @param data data to split
#' @param train_size split size
#' @return the data with a split column TRUE for train dataset FALSE test
#' @examples
#' split_data(vehicles, 0.9)
split_data <- function(data, train_size) {
  train_size <- as.double(train_size)
  data$state <- toupper(data$state)
  if (train_size >= 0 && train_size <= 1) {
    sample_size <- floor(as.double(train_size) * nrow(data))
    train_id <- sample(seq_len(nrow(data)), size = sample_size)

    train <- data[train_id,]
    test <- data[-train_id,]

    list_results <- list(train, test)
    return(list_results)
  }
  else {
    print("The train_size parameter is not valid")
  }
}


#' Prints the data the a provided paths
#'
#' @param data_path Path to print the data
#' @param data Dataset to print
#' @param replace Replace existing file or stop
#' @return Nothing
#' @examples
#' print_train_test('../data/vehicles_train.csv',vehicles_train)
print_dataset <- function(data_path, data, replace = TRUE) {
  if (file.exists(data_path) && !replace) {
    print("The file already exists")
  }
  else {
    write_csv(data, data_path)
  }
}


main(opt$DATA_FILE_PATH, opt$TRAIN_FILE_PATH, opt$TEST_FILE_PATH, opt$TARGET, opt$REMOVE_OUTLIERS, opt$TRAIN_SIZE)
