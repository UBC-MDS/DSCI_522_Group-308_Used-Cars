all: doc/used_cars_report.html doc/used_cars_report.md

data/vehicles.csv: scripts/download.py
	python scripts/download.py --DATA_FILE_PATH=data/vehicles.csv --DATA_FILE_URL=http://mds.dev.synnergia.com/uploads/vehicles.csv --DATA_FILE_HASH=06e7bd341eebef8e77b088d2d3c54585
	
data/vehicles_train.csv data/vehicles_test.csv: scripts/wrangling.R data/vehicles.csv
	Rscript scripts/wrangling.R --DATA_FILE_PATH=data/vehicles.csv --TRAIN_FILE_PATH=data/vehicles_train.csv --TEST_FILE_PATH=data/vehicles_test.csv --TARGET=price --REMOVE_OUTLIERS=YES --TRAIN_SIZE=0.9

results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png: scripts/eda.py data/vehicles_train.csv
	python scripts/eda.py --DATA_FILE_PATH=data/vehicles_train.csv --EDA_FILE_PATH=results/figures/
	
results/model.pic: scripts/train_model.py data/vehicles_train.csv
	python scripts/train_model.py

data/test_results_sample.csv: scripts/test_model.py data/vehicles_test.csv
	python scripts/test_model.py
	
doc/used_cars_report.html doc/used_cars_report.md: doc/used_cars_report.Rmd results/test_results_sample.csv
	Rscript -e "library(rmarkdown); render('doc/used_cars_report.Rmd')"

clean :
	rm -f data/vehicles.csv
	rm -f data/vehicles_train.csv data/vehicles_test.csv
	rm -f results/figures/condition.png results/figures/corrplot.png results/figures/cylinder.png results/figures/fuel.png results/figures/manufacturer.png results/figures/map_count.png results/figures/map_price.png results/figures/paint_color.png results/figures/size.png results/figures/state.png results/figures/title_status.png results/figures/transmission.png results/figures/type.png
	rm -f results/model.pic
	rm -f data/test_results_sample.csv
	rm -f doc/used_cars_report.html doc/used_cars_report.md