-- 1) 10 Dernières prédictions (join request + result)
SELECT r.created_at, r.endpoint, s.prediction, s.proba_positive, s.latency_ms
FROM app.prediction_request r
JOIN app.prediction_result s USING (request_id)
ORDER BY r.created_at DESC
LIMIT 10;

-- 2) Distribution des prédictions
SELECT prediction, COUNT(*) AS n
FROM app.prediction_result
GROUP BY prediction
ORDER BY prediction;

-- 3) Latence moyenne + proba moyenne
SELECT
  AVG(latency_ms) AS avg_latency_ms,
  AVG(proba_positive) AS avg_proba_positive
FROM app.prediction_result;

-- 4) Taille du dataset importé
SELECT COUNT(*) AS dataset_rows
FROM app.employee_dataset;