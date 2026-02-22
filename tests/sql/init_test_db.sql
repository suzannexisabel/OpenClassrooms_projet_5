CREATE SCHEMA IF NOT EXISTS app;

CREATE TABLE IF NOT EXISTS app.model_registry (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  version TEXT NOT NULL,
  artifact_path TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (name, version)
);

CREATE TABLE IF NOT EXISTS app.prediction_request (
  request_id TEXT PRIMARY KEY,
  endpoint TEXT NOT NULL,
  input_json JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS app.prediction_result (
  id SERIAL PRIMARY KEY,
  request_id TEXT NOT NULL REFERENCES app.prediction_request(request_id),
  model_id INTEGER NOT NULL REFERENCES app.model_registry(id),
  threshold DOUBLE PRECISION NOT NULL,
  proba_positive DOUBLE PRECISION NOT NULL,
  prediction INTEGER NOT NULL,
  latency_ms INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Seed indispensable : ton code cherche (employee_churn_rf, v1)
INSERT INTO app.model_registry (name, version, artifact_path)
VALUES ('employee_churn_rf', 'v1', 'TEST_ARTIFACT_PATH')
ON CONFLICT (name, version) DO NOTHING;
