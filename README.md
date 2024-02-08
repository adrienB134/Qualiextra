# Qualiextra

## Project Description
Qualiextra is a company created in 2021 to connect hotels that need immediately operational extras with extras who are looking for missions. It advocates for a qualitative approach with a simplified process and the ability to handle urgent missions.

This project meets the needs of this company, which is looking for an analysis and prediction tool to monitor its activity.

## Objectives
1. Provide Qualiextra with a complete dashboard presenting the essential elements of its activity, including:
   - Evolution of turnover and margin
   - Cash flow monitoring
   - Performance tracking of hotels and extras
2. Predict the need for extras over a given period to anticipate holidays or recruitment, for example.

These elements will be grouped together in a Streamlit application.

## Dataset
The provided dataset presents all the missions carried out by Qualiextra.
This dataset is confidential, and an NDA must be signed to access the data.

## Content
The project consists of the following folders:
1. A `.streamlit` folder for configuring the Streamlit application
2. A `pages` folder comprising all the tabs of the application
   - Business / Extras / Hotels for specific analyses of Qualiextra's activity
   - Forecast for predicting the need for extras over a given period
3. A `utils` folder containing a file governing the entire dataset preprocessing that is downloaded into the application
4. A `Dockerfile` for running the application in a Docker container
5. The `Index`: home page of the application for loading new data and visualizing some metrics and a map of the hotels
6. A `requirements.txt` file for installing the necessary packages to create the Docker image
7. Two files (`build.sh` and `run.sh`) for building and launching the application via Docker

## Usage
#### The Streamlit application can be launched locally or inside a Docker container.
First, clone the GitHub repository into a new folder:

```
git clone https://github.com/Simoncld8/LEAD_PROJECT_QUALIEXTRA.git
```
or
```
gh repo clone Simoncld8/LEAD_PROJECT_QUALIEXTRA.git
```
Then choose one of the following methods:

**Docker:**<br>
If necessary, the image can be built using the following command:

```
bash docker_build.sh
```
Then to launch the application from the container:
```
bash docker_run.sh
```

**Local :**<br>
To install the dashboard locally, use the following command in a terminal and follow the instructions:
```
bash local_install.sh
```
It will then be possible to launch the application with the command:
```
bash Qualiextra.sh
```

## Contributors

Adrien Berthélémé

Simon Claude 

Nicolas Leurs

This project was carried out as part of the "Data science and engineering Fullstack" training by Jedha to validate part of the "Machine Learning Engineer" certificate.