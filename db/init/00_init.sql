CREATE SCHEMA IF NOT EXISTS app;

-- Model

CREATE TABLE IF NOT EXISTS app.model_registry (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    artifact_path TEXT NOT NULL, 
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE(name, version)
);

-- Input reçu par l'API

CREATE TABLE IF NOT EXISTS app.prediction_request (
  id BIGSERIAL PRIMARY KEY,
  request_id UUID NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  endpoint TEXT NOT NULL,
  input_json JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_prediction_request_created_at
  ON app.prediction_request(created_at DESC);

-- Output du modele

CREATE TABLE IF NOT EXISTS app.prediction_result (
  id BIGSERIAL PRIMARY KEY,
  request_id UUID NOT NULL REFERENCES app.prediction_request(request_id),
  model_id INTEGER NOT NULL REFERENCES app.model_registry(id),

  threshold DOUBLE PRECISION NOT NULL,
  proba_positive DOUBLE PRECISION NOT NULL,
  prediction INTEGER NOT NULL,
  latency_ms INTEGER NOT NULL,

  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_prediction_result_request
  ON app.prediction_result(request_id);

-- Enregistrement du modele par défaut dans la BD si elle n'existe pas encore 
INSERT INTO app.model_registry (name, version, artifact_path)
VALUES ('employee_churn_rf', 'v1', 'models/model.joblib')
ON CONFLICT (name, version) DO NOTHING;

-- Dataset (training data)
CREATE TABLE IF NOT EXISTS app.employee_dataset (
  id BIGSERIAL PRIMARY KEY,
  
  age INTEGER NOT NULL,
  genre TEXT NOT NULL,
  poste TEXT NOT NULL,
  nombre_experiences_precedentes INTEGER NOT NULL,
  niveau_hierarchique_poste INTEGER NOT NULL,
  heure_supplementaires INTEGER NOT NULL,
  a_quitte_l_entreprise INTEGER NOT NULL CHECK (a_quitte_l_entreprise IN (0,1)),
  nombre_participation_pee INTEGER NOT NULL,
  niveau_education INTEGER NOT NULL,
  domaine_etude TEXT NOT NULL,
  ratio_anciennete_manager DOUBLE PRECISION NOT NULL,
  frequence_deplacement_code INTEGER NOT NULL,
  score_satisfaction_global DOUBLE PRECISION NOT NULL,
  delta_evaluation INTEGER NOT NULL,
  "Célibataire" INTEGER NOT NULL CHECK ("Célibataire" IN (0,1)),
  annees_dans_l_entreprise_bins INTEGER NOT NULL,
  distance_domicile_travail_bins INTEGER NOT NULL,


  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_employee_dataset_created_at
  ON app.employee_dataset(created_at DESC);