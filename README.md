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

- F-beta score : 0.629
- Recall : 75 %
- Precision : 36 %
- Seuil métier : 47 %

---

### Le projet inclut :
- une API FastAPI avec documentation Swagger/OpenAPI,
- une base PostgreSQL (local) pour la **traçabilité des prédictions** (inputs/outputs),
- des tests unitaires, fonctionnels et DB (Pytest) + couverture (pytest-cov),
- une CI (GitHub Actions) et un déploiement automatique sur Hugging Face Spaces.

---

## Architecture du dépôt
- `app/` : code FastAPI (API, schémas Pydantic, accès DB, chargement modèle)
- `db/init/00_init.sql` : initialisation PostgreSQL (schéma + tables)
- `tests/` : tests Pytest (unitaires / fonctionnels / DB)
- `Dockerfile`, `docker-compose.yml` : exécution locale / déploiement HF (Docker SDK)
- `.github/workflows/` : CI + déploiement Hugging Face
- `docs/` : schéma UML de la base de données
- `data/` : Données d'apprentissage du modèle (.csv)
- `db/` : exemple de requêtes SQL sur la base de donnée
- `sql/` : initialisation de la base de données test
- `scripts/`

---

## Lancer le projet en local
---
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

```Bash
docker-compose up -d
```
---
#### Variables d’environnement

Le projet utilise des variables d’environnement pour activer ou désactiver la base de données.
Si la variable d’environnement `DATABASE_URL` n’est pas définie,
l’API démarre en mode sans base de données (pas de logging des prédictions).

---
#### Activer la DB en Local 

```Bash
export DATABASE_URL=postgresql+psycopg://mluser:mlpass@localhost:5432/mldb  
export DATABASE_URL_TEST=postgresql+psycopg://mluser:mlpass@localhost:5432/mldb_test  
```
--- 

#### Shéma de la base de données (UML)

Voici le diagramme qui représente la structure et les relations de la base de données PostgreSQL.

![Database Shema](docs/uml_db.png)

### Tables Principales 
- `app.model_registry` : registre des versions du modèle (nom, version, artifact_path)
- `app.prediction_request` : logs des inputs (payload JSON)
- `app.prediction_result` : logs des outputs (prediction, proba, seuil, latence) + FK vers request et modèle
- `app.employee_dataset` : représente la base de données d'apprentissage du modèle RF. 

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

## Déploiement sur Hugging Face Space

[Hugging Face Space](https://huggingface.co/spaces/suzannexisabel/HF_space_OC_projet_5)