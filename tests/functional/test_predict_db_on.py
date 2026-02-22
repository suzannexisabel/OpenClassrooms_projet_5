import pytest
from sqlalchemy import text

@pytest.mark.db
def test_predict_logs_to_db(client_with_db, test_engine):
    payload = {
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
        "domaine_etude": "Ressources Humaines",
    }

    with test_engine.begin() as conn:
        n_req_before = conn.execute(text("SELECT COUNT(*) FROM app.prediction_request")).scalar_one()
        n_res_before = conn.execute(text("SELECT COUNT(*) FROM app.prediction_result")).scalar_one()

    r = client_with_db.post("/predict", json=payload)
    assert r.status_code == 200

    with test_engine.begin() as conn:
        n_req_after = conn.execute(text("SELECT COUNT(*) FROM app.prediction_request")).scalar_one()
        n_res_after = conn.execute(text("SELECT COUNT(*) FROM app.prediction_result")).scalar_one()

    assert n_req_after == n_req_before + 1
    assert n_res_after == n_res_before + 1