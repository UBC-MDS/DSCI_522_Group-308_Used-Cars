# authors: Andres Pitta, Braden Tam, Serhiy Pokrovskyy
# date: 2020-02-05

# This Dockerfile defines the environment for container to run this project.

# Base from anaconda3
FROM continuumio/anaconda3

# Update APT and install necessary system packages / prerequisites
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y autoconf automake gdb git libffi-dev zlib1g-dev libssl-dev curl libcurl4-openssl-dev libxml2-dev orca xvfb wget r-base r-base-dev libnss3 unzip chromium libgtk2.0 libgtk2.0-dev libgconf-2-4

# Install chromedriver
RUN wget -q "https://chromedriver.storage.googleapis.com/79.0.3945.36/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip && chown root:root /usr/bin/chromedriver && chmod +x /usr/bin/chromedriver

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Install Python packages
RUN pip install docopt numpy pandas sklearn statsmodels xgboost lightgbm plotly altair selenium psutil requests plotly orca flask pygments

# Install orca with plotly
RUN conda install -y -c plotly plotly-orca

# Install R packages
RUN Rscript -e "install.packages(c('tidyverse', 'docopt', 'kableExtra'))"