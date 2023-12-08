# Qualiextra

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
