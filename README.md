# Qualiextra

*English below.*

## Description du projet
Qualiextra est une société créée en 2021 de mise en relation d'hôtels qui ont un besoin d’extras immédiatement opérationnels et d'extras qui sont à la recherche de missions. Elle prône une approche qualitative avec une démarche simplifiée avec la possibilité de prendre en charge des missions urgentes. 

Ce projet répond aux besoins de cette société qui recherche un outil d'analyse et de prédiction pour le suivi de son activité. 

## Objectifs
1. Fournir à la société Qualiextra un dahsboard complet présentant les éléments essentiels de son activité avec notamment :
   - évolution du chiffre d'affaires et de la marge
   - suivi de la trésorerie 
   - suivi de la performance des hôtels et des extras
2. Prédire le besoin en Extras sur une période donnée afin d'anticiper les congés ou les recrutements par exemple.

Ces éléments seront regroupés dans une application Streamlit. 


## Dataset
Le dataset fourni présente l'ensemble des missions effectuées par Qualiextra. 
Ce dataset est confidentiel, un NDA doit être signé pour accéder aux données. 

## Contenu
Le projet se compose des dossiers suivants : 
1. Un dossier .streamlit permettant de configurer l'application Streamlit
2. Un dossier pages comprenant l'ensemble des onglets de l'application
   - Business / Extras / Hotels pour les analyses spécifiques de l'activité de Qualiextra
   - Forecast pour la prédiction du besoin en extras sur une période donnée
3. Un dossier utils comprenant un fichier régissant l'ensemble du preprocessing du dataset qu'on télécharge dans l'application
4. Un Dockerfile permettant de faire fonctionner l'application dans un conteneur Docker
5. L'Index : page d'accueil de l'application permettant de charger les nouvelles données et également de visualiser de quelques métrics et une cartographie des hôtels
6. Un fichier requirements.txt permettant l'installation des packages nécessaires à la création de l'image Docker
7. Deux fichiers (build.sh et run.sh) permettant de construire et de lancer l'application via un Docker


## Usage
#### L'application streamlit peut être lancée en local ou à l'intérieur d'un conteneur docker
Tout d'abord clonez le github dans un nouveau dossier :
```
git clone https://github.com/adrienB134/Qualiextra.git
```
ou
```
gh repo clone adrienB134/Qualiextra
```
Puis choisissez l'une des méthodes suivante:

**Docker :**<br>
Si nécessaire il est possible de construire l'image à l'aide de la commande suivante.
```
bash docker_build.sh
```
Puis pour lancer l'application depuis le conteneur:
```
bash docker_run.sh
```

**Local :**<br>
Pour installer le dashboard en local, utilisez la commande suivante dans un terminal et suivez les instructions:
```
bash local_install.sh
```
Il sera ensuite possible de lancer l'application avec la commande:
```
bash Qualiextra.sh
```

## Contributeurs

Adrien Berthélémé

Simon Claude 

Nicolas Leurs

Ce projet a été réalisé dans le cadre de la formation "Data science and engineering Fullstack" de Jedha afin de valider une partie du certificat "Concepteur Développeur en Science des données".



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
git clone https://github.com/adrienB134/Qualiextra.git
```
or
```
gh repo clone adrienB134/Qualiextra
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
