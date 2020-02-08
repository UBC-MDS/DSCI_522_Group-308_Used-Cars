# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-02-05

# This Dockerfile defines the environment for container to run this project.

# Base from current stable Debian Linux
# TODO: affix Debian major version!
FROM debian:stable

# Update APT and install necessary system packages / prerequisites
RUN apt-get update -y
RUN apt-get install -y r-base r-base-dev
RUN apt-get install -y build-essential
RUN apt-get install -y autoconf automake gdb git libffi-dev zlib1g-dev libssl-dev curl libcurl4-openssl-dev libxml2-dev orca xvfb wget

# Install Python
RUN apt-get install -y python python3
RUN apt-get install -y python-pip python3-pip
# Fix python3 to become new system default python instead of python2
RUN update-alternatives --install /usr/bin/python python /usr/bin/python2 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip2 1
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 2

RUN apt-get update && apt install -y chromium && apt-get install -y libnss3 && apt-get install unzip

# Install chromedriver
RUN wget -q "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip && chown root:root /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb


# Install Python dependencies
RUN pip install docopt numpy pandas sklearn statsmodels xgboost lightgbm plotly altair selenium psutil requests plotly orca flask pygments

# Install R dependencies
RUN Rscript -e "install.packages(c('tidyverse', 'docopt', 'kableExtra', 'knitr'))"


# Make the project
# RUN make quick

# TODO: install Selenium and make the rest of `make` work! (EDA / report generation)