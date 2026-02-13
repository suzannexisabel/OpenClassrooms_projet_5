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