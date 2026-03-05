---
title: OC_projet_5_API
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# OpenClassrooms Project 5 – Déploiement d'un modèle de machine learning avec FastAPI

## Objectif
Ce projet fournit un **Proof of Concept (POC)** de déploiement d’un modèle de machine learning permettant de prédire le risque de départ d'un employé.
Le modèle est basé sur un Random Forest optimisé qui identifie les employés susceptibles de quitter l’entreprise afin d’anticiper les risques de turnover et d’accompagner la prise de décision des équipes Ressources Humaines.

Le modèle est exposé via une **API FastAPI**, et déployé sur Hugging Face Spaces. L’API expose un endpoint `/predict` qui renvoie une prédiction (classe) et une probabilité associée.

---
### Performances finales du modèle

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| F-beta score | 0.629 | Compromis optimisé entre précision et rappel |
| Recall | 75 % | 75 % des employés qui quittent l’entreprise sont correctement détectés |
| Precision | 36 % | Parmi les employés prédits comme partants, 36 % quittent réellement |
| Seuil de décision | 0.47 | Seuil ajusté pour privilégier la détection des départs |

---

### Le projet inclut :
- une API FastAPI avec documentation Swagger/OpenAPI,
- une base PostgreSQL (local) pour la **traçabilité des prédictions** (inputs/outputs),
- des tests unitaires, fonctionnels et DB (Pytest) + couverture (pytest-cov),
- une CI (GitHub Actions) et un déploiement automatique sur Hugging Face Spaces.

---

## Architecture du dépôt
```bash
.
├── app/                         # Application FastAPI
│   ├── main.py                  # Endpoints API (/ , /health , /predict)
│   ├── db.py                    # Connexion PostgreSQL via SQLAlchemy
│   ├── model.py                 # Chargement du pipeline ML (joblib ou download HF)
│   └── schemas.py               # Schémas Pydantic (requêtes / réponses)
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # Pipeline CI/CD GitHub Actions
│
├── tests/                       # Tests automatisés Pytest
│   ├── functional/              # Tests fonctionnels de l'API
│   │   ├── test_health.py
│   │   ├── test_predict_db_off.py
│   │   ├── test_predict_db_on.py
│   │   ├── test_predict_rollback.py
│   │   └── test_root.py
│   │
│   ├── unit/                    # Tests unitaires des composants
│   │   ├── test_predict_classes.py
│   │   ├── test_predict_errors.py
│   │   ├── test_predict_threshold.py
│   │   ├── test_schemas.py
│   │   └── test_smoke.py
│   │
│   ├── sql/                     # Scripts SQL pour les tests DB
│   │   └── init_test_db.sql
│   │
│   └── conftest.py              # Fixtures Pytest partagées
│
├── db/                          # Scripts SQL PostgreSQL
│   ├── init/
│   │   └── 00_init.sql          # Création du schéma et des tables
│   └── examples_queries.sql     # Exemples de requêtes SQL
│
├── scripts/                     # Scripts utilitaires
│   ├── import_dataset.py        # Import du dataset dans PostgreSQL
│   └── query_db_stats.py        # Requêtes statistiques sur la base
│
├── docs/                        # Documentation technique
│   ├── model_documentation.md   # Documentation du modèle
│   ├── uml_db.png               # Diagramme UML de la base
│   └── uml_db.puml              # Source PlantUML du diagramme
│
├── data/                        # Données d'apprentissage
│   └── employee_churn_dataset_for_db.csv
│
├── docker-compose.yml           # Lancement PostgreSQL local
├── Dockerfile                   # Image Docker de l'API
├── pytest.ini                   # Configuration Pytest
├── README.md                    # Documentation principale
├── requirements.txt             # Dépendances Python
├── .gitattributes
└── .gitignore
```

## Lancer le projet en local
---

### 0) Cloner le dépôt

```bash
git clone https://github.com/suzannexisabel/OpenClassrooms_projet_5.git
cd OpenClassrooms_projet_5
```

### 1) Installation python
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```
---
### 2) Lancer l'API 

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Swagger UI : `http://localhost:8000/docs`
- Health check : `http://localhost:8000/health`

---
### 3) Base de données (PostgreSQL)

La base est utilisée en local pour logger les requêtes et résultats de prédiction.
En déploiement cloud (Hugging Face Spaces), la base de données n'est pas connectée mais l’API fonctionne parfaitement sans.

---
#### Démarrer PostgreSQL via Docker

```bash
docker-compose up -d
```
---
#### Variables d’environnement

Le projet utilise des variables d’environnement pour activer ou désactiver la base de données.
Si la variable d’environnement `DATABASE_URL` n’est pas définie,
l’API démarre en mode sans base de données (pas de logging des prédictions).

---
#### Activer la DB en Local 

```bash
export DATABASE_URL=postgresql+psycopg://mluser:mlpass@localhost:5432/mldb  
export DATABASE_URL_TEST=postgresql+psycopg://mluser:mlpass@localhost:5432/mldb_test  
```
--- 

#### Schéma de la base de données (UML)

Voici le diagramme qui représente la structure et les relations de la base de données PostgreSQL.

![Database Schema](docs/uml_db.png)

### Tables Principales 
- `app.model_registry` : registre des versions du modèle (nom, version, artifact_path)
- `app.prediction_request` : logs des inputs (payload JSON)
- `app.prediction_result` : logs des outputs (prediction, proba, seuil, latence) + FK vers request et modèle
- `app.employee_dataset` : représente la base de données d'apprentissage du modèle RF. 

## API en ligne 

[L’API est accessible ici](https://huggingface.co/spaces/suzannexisabel/HF_space_OC_projet_5)

## API - endpoints

- `GET /`
Page d’accueil avec liens vers /docs et /health.
- `GET /health`
Vérifie que l’API est active et que le modèle est chargeable.
- `POST /predict`
Entrée : payload validé par Pydantic (PredictRequest)
Sortie : prediction (0/1) et probability (proba classe positive).

### Exemple d'appel 
 ```bash
 curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "nombre_experiences_precedentes": 2,
    "niveau_hierarchique_poste": 2,
    "heure_supplementaires": 0,
    "nombre_participation_pee": 1,
    "niveau_education": 3,
    "frequence_deplacement_code": 1,
    "delta_evaluation": 1,
    "annees_dans_l_entreprise_bins": 2,
    "distance_domicile_travail_bins": 1,
    "Célibataire": 1,
    "ratio_anciennete_manager": 0.6,
    "score_satisfaction_global": 3.5,
    "genre": "F",
    "poste": "Manager",
    "domaine_etude": "Ressources Humaines"
  }'
 ```

## Chargement du Modèle ML 

Le modèle est chargé via `app/model.py` :
- priorité à `models/model.joblib` (en local),
- sinon téléchargement depuis Hugging Face Hub via `HF_TOKEN`.

Variables :
`HF_TOKEN` : token Hugging Face (requis si le fichier local est absent)

## Tests et couverture

### Lancer les tests 

#### 1) Tests unitaires 
```bash
pytest -m unit -vv
```

#### 2) Test fonctionnels 
```bash
pytest -m functional -vv
```
#### 3) Test base de données (`PostgreSQl` requis, variable `DATABASE_URL_TEST` définie)

```bash
pytest -m db -vv
```

### Rapport de Couverture

#### 1) Sans base de données (DB OFF)
```bash
pytest -m "not db" -vv --cov=app --cov-report=term-missing --cov-report=xml
```

#### 2) Avec base de données (DB ON)
```bash
pytest -vv --cov=app --cov-report=term-missing --cov-report=xml
```

## CI/CD avec GitHub Actions

- CI : exécute automatiquement les tests (DB OFF + DB ON) et génère un rapport de couverture uploadé en artifact.
- CD : déploie automatiquement sur Hugging Face Spaces à chaque push sur `main` avec le `TOKEN` via GitHub Secrets.

## Sécurité et gestion des accès
Les informations sensibles ne sont jamais stockées dans le dépôt.

Les variables suivantes sont utilisées pour gérer l’accès aux ressources :

- `DATABASE_URL`
- `DATABASE_URL_TEST`
- `HF_TOKEN`

Ces variables sont :

- définies dans un fichier `.env` en local (non versionné),
- stockées dans **GitHub Secrets** pour la CI/CD.

Bonnes pratiques appliquées :

- le fichier `.env` est ignoré via `.gitignore`
- les tokens et identifiants ne sont jamais committés dans le dépôt
- les accès aux services externes passent uniquement par des variables d’environnement.

## Déploiement sur Hugging Face Space

[Hugging Face Space](https://huggingface.co/spaces/suzannexisabel/HF_space_OC_projet_5)

## Documentation supplémentaire

- [Documentation technique du modèle](docs/model_documentation.md)