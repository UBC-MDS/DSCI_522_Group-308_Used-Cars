# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-30

# This Makefile build the project - from downloading data through training / testing models and to generating final reports.
#
# This Makefile defines 3 main targets:
# $> make all						builds everything on a full dataset (~400,000 train observations)
# $> make quick						builds everything on a 1% of original dataset
# $> make quick TRAIN_SIZE=0.05		builds everything on arbitary % of the dataset (eg. 5%)
# $> make clean						cleanup / reset
# $> make partial_clean				cleanup / reset, keeping original data file
# $> make all_docker				Same as `make all`, but using Docker
# $> make quick_docker				Same as `make quick`, but using Docker
#
# NOTE: be advised that this will have to download 1.35 GB datafile! Consult README.md for more details

### Main targets ###

all : results/model.pic doc/used_cars_report.html doc/used_cars_report.md
quick : test_quick_model doc/used_cars_report.html doc/used_cars_report.md

### Defaults ###

TRAIN_SIZE=0.01

### General dependencies ###

# Download
data/vehicles.csv:
	@echo ">>> Running download script..."
	python scripts/download.py --DATA_FILE_PATH=data/vehicles.csv --DATA_FILE_URL=http://mds.dev.synnergia.com/uploads/vehicles.csv --DATA_FILE_HASH=06e7bd341eebef8e77b088d2d3c54585

# Wrangling
data/vehicles_train.csv data/vehicles_test.csv: data/vehicles.csv
	@echo ">>> Running data wrangling script..."
	Rscript scripts/wrangling.R --DATA_FILE_PATH=data/vehicles.csv --TRAIN_FILE_PATH=data/vehicles_train.csv --TEST_FILE_PATH=data/vehicles_test.csv --TARGET=price --REMOVE_OUTLIERS=YES --TRAIN_SIZE=0.8

# Full model
results/model.pic: data/vehicles_train.csv
	@echo ">>> Building full model..."
	python scripts/train_model.py --TRAIN_SIZE=1 --MODEL_DUMP_PATH=results/model.pic

# Test model
results/test_results_sample.csv: data/vehicles_test.csv
	@echo ">>> Testing model..."
	python scripts/test_model.py --TEST_SIZE=1 --MODEL_DUMP_PATH=results/model.pic

# EDA plots
results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png: data/vehicles_train.csv
	@echo ">>> Running EDA..."
	python scripts/eda.py --DATA_FILE_PATH=data/vehicles_train.csv --EDA_FILE_PATH=results/figures/

# Report
doc/used_cars_report.html doc/used_cars_report.md: doc/used_cars_report.Rmd results/test_results_sample.csv results/figures/condition.png
	@echo ">>> Generating report..."
	Rscript -e "library(rmarkdown); render('doc/used_cars_report.Rmd')"

### Quick model ###

results/model_quick.pic: data/vehicles_train.csv
	@echo ">>> Building quick model..."
	python scripts/train_model.py --TRAIN_SIZE=$(TRAIN_SIZE) --MODEL_DUMP_PATH=results/model_quick.pic

test_quick_model: results/model_quick.pic
	@echo ">>> Testing quick model..."
	python scripts/test_model.py --TEST_SIZE=1 --MODEL_DUMP_PATH=results/model_quick.pic

### Docker shortcuts targets ###

quick_docker:
	docker run --rm -v /$(PWD):/home pokrovskyy/dsci-522-308-used-cars bash -c "make -C /home quick TRAIN_SIZE=$(TRAIN_SIZE)"

all_docker:
	docker run --rm -v /$(PWD):/home pokrovskyy/dsci-522-308-used-cars bash -c "make -C /home all"

### Cleanup ###

clean :
	@echo ">>> Full clean up..."
	rm -f data/vehicles.csv
	rm -f data/vehicles_train.csv data/vehicles_test.csv
	rm -f results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png results/figures/cylinders.png
	rm -f results/model.pic
	rm -f results/model_quick.pic
	rm -f results/test_results_sample.csv
	rm -f results/test_metrics.csv
	rm -f results/train_metrics.csv
	rm -f doc/used_cars_report.html doc/used_cars_report.md
	
partial_clean :
	@echo ">>> Partial clean up..."
	rm -f data/vehicles_train.csv data/vehicles_test.csv
	rm -f results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png results/figures/cylinders.png
	rm -f results/model.pic
	rm -f results/model_quick.pic
	rm -f results/test_results_sample.csv
	rm -f results/test_metrics.csv
	rm -f results/train_metrics.csv
	rm -f doc/used_cars_report.html doc/used_cars_report.md