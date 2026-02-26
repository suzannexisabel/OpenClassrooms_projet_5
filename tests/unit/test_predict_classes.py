import pytest
from app.schemas import PredictRequest

def make_payload_obj() -> PredictRequest:
    return PredictRequest(
        age=35,
        nombre_experiences_precedentes=2,
        niveau_hierarchique_poste=2,
        heure_supplementaires=0,
        nombre_participation_pee=1,
        niveau_education=3,
        frequence_deplacement_code=1,
        delta_evaluation=1,
        annees_dans_l_entreprise_bins=2,
        distance_domicile_travail_bins=1,
        celibataire=1,
        ratio_anciennete_manager=0.6,
        score_satisfaction_global=3.5,
        genre="F",
        poste="Manager",
        domaine_etude="Ressources Humaines",
    )

@pytest.mark.unit
def test_positive_class_index_when_classes_reversed(mock_model_factory):
    from app import main
    # classes inversées: [1,0] => index(1)=0
    mock_model_factory(proba_positive=0.6, classes=(1, 0))

    payload = make_payload_obj()
    res = main.predict(payload=payload, db=None)

    assert res.prediction == 1
    assert abs(res.probability - 0.6) < 1e-12
