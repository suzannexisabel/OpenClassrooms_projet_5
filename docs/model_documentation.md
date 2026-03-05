# Documentation technique du modèle de Machine Learning 

## Objectif
Le modèle développé dans ce projet vise à prédire le risque de départ d’un employé au sein d’une entreprise.
L’objectif est d’identifier les employés susceptibles de quitter l’organisation afin de permettre aux équipes Ressources Humaines :
- d’anticiper les risques de turnover,
- d’identifier les facteurs associés aux départs,
- de mettre en place des actions de rétention ciblées.

Le modèle est exposé via une API FastAPI et déployé sur Hugging Face Spaces, permettant d’effectuer des prédictions à partir de caractéristiques individuelles des employés.

## Nature du modèle 

Le modèle repose sur un **Random Forest Classifier**, un algorithme d’apprentissage basé sur un ensemble d’arbres de décision.

Un Random Forest est un ensemble de plusieurs arbres de décision. Chaque arbre produit une prédiction, et la prédiction finale est déterminée par la classe la plus fréquemment prédite par l’ensemble des arbres.

## Données

Le modèle a été entraîné sur un jeu de données décrivant différentes caractéristiques liées :
- aux caractéristiques individuelles des employés,
- à leur poste et environnement de travail,
- à leur historique professionnel.

La variable cible est :
- `a_quitte_l_entreprise`
 
| Valeur   | Signification                    |
|----------|----------------------------------|
|0         |L'employé reste dans l'entreprise |
|1         | L'employé quitte l'entreprise.   |

### Exemple de variables utilisées
---
Les variables utilisées dans le modèle sont issues de données RH décrivant le profil des employés, leur poste et leur comportement au travail.
**Caractéristiques individuelles**
- âge
- genre
- niveau d’éducation
- situation familiale

**Caractéristiques professionnelles**
- poste
- niveau hiérarchique
- domaine d’étude

**Historique professionnel**
- nombre d’expériences précédentes
- ancienneté dans l’entreprise
- distance domicile-travail

**Indicateurs de performence et de satisfaction**
- évolution
- score de satisfaction global
- participation à des dispositifs d’épargne salariale

## Prétraitement des données 

Avant l’entraînement du modèle, les données sont prétraitées à l’aide d’un pipeline scikit-learn.

Les principales étapes sont :
**Encodage des variables catégorielles**
Les variables catégorielles sont transformées en variables numériques à l’aide d’un encodage approprié afin d’être utilisables par l’algorithme de machine learning.
**Gestion des variables numériques**
Les variables numériques sont standardisées à l’aide d’un **StandardScaler** afin d’harmoniser leur échelle.  
Bien que cette transformation ne soit pas indispensable pour un modèle basé sur des arbres de décision comme la Random Forest, elle est conservée dans le pipeline afin de maintenir une structure de prétraitement cohérente et reproductible.

**Pipeline**
Le pipeline comprend :
- les étapes de prétraitement,
- l’algorithme de classification.
Cela permet de garantir que les mêmes transformations sont appliquées en production lors des prédictions.

## Ooptimisatio du modèle
Les hyperparamètres du modèle ont été optimisés via une recherche d’hyperparamètres.
La métrique utilisée pour sélectionner le meilleur modèle est le F-beta score.
Cette métrique permet de privilégier la détection des employés à risque de départ, ce qui correspond à l’objectif métier.

## performences

Les performences du modele optimisé sont :

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| F-beta score | 0.629 | Compromis optimisé entre précision et rappel |
| Recall | 75 % | 75 % des employés qui quittent l’entreprise sont correctement détectés |
| Precision | 36 % | Parmi les employés prédits comme partants, 36 % quittent réellement |
| Seuil de décision | 0.47 | Seuil ajusté pour privilégier la détection des départs |

**Le seuil de décision a été ajusté à :**
0.47

**Ce choix permet :**
- la détection des employés susceptibles de quitter l’entreprise (aun moins 75%)
- au prix d’un nombre plus élevé de faux positifs.

Dans ce contexte métier, il est plus coûteux pour l’entreprise de **ne pas détecter un employé susceptible de quitter l’entreprise** (faux négatif) que d’identifier à tort un employé comme étant à risque (faux positif). Un faux négatif correspondrait à un départ non anticipé, pouvant entraîner des coûts importants liés au recrutement, à la perte de compétences et à la désorganisation des équipes. À l’inverse, un faux positif peut simplement conduire les équipes RH à analyser plus attentivement une situation ou à mettre en place des actions préventives> Pour cette raison, le modèle privilégie le **recall**, afin de détecter le plus grand nombre possible d’employés susceptibles de quitter l’entreprise.

## Déploiement du modèle
Le modèle entraîné est exporté au format : `joblib`
Il est ensuite utilisé dans l’API FastAPI.

Le chargement du modèle suit la logique suivante :
Chargement du fichier local models/model.joblib
Si le fichier n’est pas présent, téléchargement depuis Hugging Face Modèle