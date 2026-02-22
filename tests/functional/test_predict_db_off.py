import pytest

@pytest.mark.functional
def test_predict_contract(client):
    payload = {}
    r = client.post("/predict", json=payload)
    assert r.status_code == 422
    body = r.json()
    assert "detail" in body

@pytest.mark.functional
def test_predict_ok(client, mock_model):
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
    r=client.post("/predict",json=payload)
    assert r.status_code == 200
    
    body = r.json()
    assert isinstance(body, dict)
    assert len(body) > 0

    # plus tard il faut tester 
    # assert "prediction" in body
    # assert "probability" in body