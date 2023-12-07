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
#### L'application streamlit peut être lancée en local ou à l'intérieur d'un contenaire docker

**Contenaire:**
Pour lancer le dashboard dans un contenaire, il suffit de clonner le github dans un nouveau dossier et de lancer la commande suivante :
```
bash build.sh && bash run.sh
```

**Local run:**
Pour lancer le dashboard en local, assurez-vous d'installer les paquets nécésaires figurant dans requirements.txt.
Clonnez ensuite le github dans un nouveau dossier et de lancer la commande suivante :
```
python -m streamlit run --server.port 4000 Index.py
```

## Contributeurs

Adrien Berthélémé

Simon Claude 

Nicolas Leurs

Ce projet a été réalisé dans le cadre de la formation "Data science and engineering Fullstack" de Jedha afin de valider une partie du certificat "Concepteur Développeur en Science des données"
This project was made as part of the Jedha Bootcamp  course and was submitted to validate part of the French certificate "Machine Learning Engineer".

## Licence
