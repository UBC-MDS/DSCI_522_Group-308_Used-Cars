# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-01-30

# This Makefile build the project - from downloading data through training / testing models and to generating final reports.
#
# This Makefile defines 3 main targets:
# $> make all     builds everything on a full dataset (~400,000 train observations)
# $> make quick   builds everything on a 1% of original dataset
# $> make clean   cleanup / reset
#
# NOTE: Eitehr way the whole 1.4GB  dataset will have to be downloaded

# Main targets

all : doc/used_cars_report.html doc/used_cars_report.md
quick : test_quick_model doc/used_cars_report.html doc/used_cars_report.md

# Dependencies

data/vehicles.csv:
	@echo ">>> Running download script..."
	python scripts/download.py --DATA_FILE_PATH=data/vehicles.csv --DATA_FILE_URL=http://mds.dev.synnergia.com/uploads/vehicles.csv --DATA_FILE_HASH=06e7bd341eebef8e77b088d2d3c54585

data/vehicles_train.csv data/vehicles_test.csv: data/vehicles.csv
	@echo ">>> Running data wrangling script..."
	Rscript scripts/wrangling.R --DATA_FILE_PATH=data/vehicles.csv --TRAIN_FILE_PATH=data/vehicles_train.csv --TEST_FILE_PATH=data/vehicles_test.csv --TARGET=price --REMOVE_OUTLIERS=YES --TRAIN_SIZE=0.8

results/model.pic: data/vehicles_train.csv
	@echo ">>> Building full model..."
	python scripts/train_model.py --TRAIN_SIZE=1 --MODEL_DUMP_PATH=results/model.pic

data/test_results_sample.csv: data/vehicles_test.csv
	@echo ">>> Testing model..."
	python scripts/test_model.py --TEST_SIZE=1 --MODEL_DUMP_PATH=results/model.pic

results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png: scripts/eda.py data/vehicles_train.csv
	@echo ">>> Running EDA..."
	python scripts/eda.py --DATA_FILE_PATH=data/vehicles_train.csv --EDA_FILE_PATH=results/figures/

doc/used_cars_report.html doc/used_cars_report.md: doc/used_cars_report.Rmd results/test_results_sample.csv
	@echo ">>> Generating report..."
	Rscript -e "library(rmarkdown); render('doc/used_cars_report.Rmd')"

# Quick model targets

results/model_quick.pic: data/vehicles_train.csv
	@echo ">>> Building quick model..."
	python scripts/train_model.py --TRAIN_SIZE=0.01 --MODEL_DUMP_PATH=results/model_quick.pic

test_quick_model: results/model_quick.pic
	@echo ">>> Testing quick model..."
	python scripts/test_model.py --TEST_SIZE=1 --MODEL_DUMP_PATH=results/model_quick.pic

# Cleanup

clean :
	@echo ">>> Cleaning up..."
	rm -f data/vehicles.csv
	rm -f data/vehicles_train.csv data/vehicles_test.csv
	rm -f results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png
	rm -f results/model.pic
	rm -f results/model_quick.pic
	rm -f data/test_results_sample.csv
	rm -f doc/used_cars_report.html doc/used_cars_report.md