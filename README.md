---
title: OC_projet_5_API
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# OpenClassrooms Project 5 – deploye un modele de machine learning

## Description
This project deploys a machine learning model using a web API.

## Project structure
- requirements.txt
- README.md

## Installation

```bash
pip install -r requirements.txt
```

## Shémas de la base de donnée

```mermaid
erDiagram

MODEL_REGISTRY {
    int id PK
    text name
    text version
    text artifact_path
    timestamptz created_at
}

PREDICTION_REQUEST {
    bigint id PK
    uuid request_id UNIQUE
    timestamptz created_at
    text endpoint
    jsonb input_json
}

PREDICTION_RESULT {
    bigint id PK
    uuid request_id FK
    int model_id FK
    float threshold
    float proba_positive
    int prediction
    int latency_ms
    timestamptz created_at
}

PREDICTION_REQUEST ||--o{ PREDICTION_RESULT : "has"
MODEL_REGISTRY ||--o{ PREDICTION_RESULT : "used_by"
```

