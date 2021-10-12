# Data-Engineer

## Objectif
L'objectif de ce projet est de mettre en place une API permettant de prédire la probabilité d'occurrence d'une fraude sur un site d'achat en ligne.

Le projet comporte 3 dossiers:

 - train
 - FastAPI
 - kubernetes

Je fais le choix d'installer tous les requirements d'un coup dans un environnement dédié:
'''
pip install -r requirements.txt
'''

## Train
Pour lancer l'entrainement du modèle de machine learning, placez vous dans le dossier train puis exécutez le script model.py:
'''
cd training
python3 model.py
'''

Le script model.py entraine un [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), affiche les métriques ([classifcation_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html), [confusion_matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html), [f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)) sur les ensembles de train et de test, et enregistre le modèle entrainé au format [pickle](https://docs.python.org/3/library/pickle.html) (model.pkl) ainsi que les métriques associées (scores.txt) dans le dossier data.


## FastAPI
Après avoir entrainé le modèle de ML, nous souhaitons développer une API HTTP permettant d'interagir avec le modèle afin d'obtenir une prédiction à partir des features.

Cette API est développée avec le framework [FastAPI](https://fastapi.tiangolo.com/) dans le dossier FastAPI. Elle est composée des fichiers suivants :

 - FastAPI_projet_2.py: fichier principal, qui définit la route de prediction POST /prediction.
 - donnees.py : définit les modèles de données attendus en entrée et sortie de l'API.
 - users.json : liste des username / password pour l'authentification.
 - data_preparation.py : Définit la fonction prepare_data, qui permet de préparer les données pour la prédiction par le modèle de ML à partir des informations transmises dans le corps de la requête POST /prediction.
 - data/model.pkl : le modèle de ML entrainé, au format pickle.

Pour lancer l'API, exécutez les commandes suivantes :
'''
cd FastAPI
uvicorn FastAPI_projet_2:api
'''

Le modèle est chargée au lancement de l'API.
L'API est désormais accessible à l'adresse [localhost:8000](http://localhost:8000/).

![image](https://user-images.githubusercontent.com/62895586/136953713-8350ade9-2a60-4cbe-bc3e-72c0ea6c5d12.png)

Afin de remplir les différentes features de l'API, voici un exemple:
'''
{
  "user_id": 2930920,
  "signup_time": "2021-07-21 18:52:44",
  "purchase_time": "2021-07-21 18:52:45",
  "purchase_value":44,
  "device_id": "YSSKYOSJHPPLJ",
  "source": "SEO",
  "browser": "Chrome",
  "sex": "M",
  "age": 35,
  "ip_address": 1120619336.0
}
'''
Vous obtiendrez le résultat suivant:
'''
{
  "prediction": 1,
  "proba": 0.7819
}
'''

### Docker
Dans le dossier FastAPI, j'ai un fichier **Dockerfile** pour créer une image docker que je nomme **christophemc/fraud_api:latest** et ainsi pouvoir lancer l'API dans un container avec la commande suivante:
'''
docker container run christophemc/fraud_api:latest
'''

## kubernetes
Dans le dossier kubernetes, j'ai enregistré les fichiers nécessaires pour déployer mon API à grande échelle avec l'image docker précédemment créée.
Pour le déploiement des pods, tapez la commande suivante:
'''
kubectl create -f my-deployment-api.yml
'''

Pour exposer leport de l'API à l'intérieur du container, nous devons créer un service avec la commande suivante:
'''
kubectl create -f my-service-api.yml
'''

Puis pour l'exposer à l'extérieur du container, nous créons un ingress avec la commande suivante:
'''
kubectl create -f my-ingress-api.yml
'''

L'API est désormais disponible à l'adresse suivante:

  [make_prediction](http://192.168.49.2/docs#/default/make_prediction_prediction_post)
