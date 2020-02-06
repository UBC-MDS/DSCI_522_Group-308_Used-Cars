# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-02-05

# This Dockerfile defines the environment for container to run this project.

# Base from current stable Debian Linux
# TODO: affix Debian major version!
FROM debian:stable

#Update APT and install necessary system packages / prerequisites
RUN apt-get update -y
RUN apt-get install -y r-base r-base-dev
RUN apt-get install -y build-essential
RUN apt-get install -y autoconf automake gdb git libffi-dev zlib1g-dev libssl-dev curl libcurl4-openssl-dev libxml2-dev

# Install Python
RUN apt-get install -y python python3
RUN apt-get install -y python-pip python3-pip
# Fix python3 to become new system default python instead of python2
RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2

# Install Python dependencies
RUN pip install docopt numpy pandas sklearn altair statsmodels xgboost lightgbm plotly selenium

# Install R dependencies
RUN Rscript -e "install.packages(c('tidyverse', 'docopt'))"

# Clone project repo
RUN mkdir -p /home/projects
RUN cd /home/projects
RUN git clone https://github.com/pokrovskyy/DSCI_522_Group-308_Used-Cars.git used-cars
RUN cd used-cars

# Make the project
# RUN make quick

# TODO: install Selenium and make the rest of `make` work! (EDA / report generation)