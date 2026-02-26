import pytest 
from fastapi import HTTPException
from pydantic import ValidationError

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
def test_value_error_becomes_400(mock_model_factory):
    from app import main
    mock_model_factory(raise_exc=ValueError("bad input"))

    payload = make_payload_obj()

    with pytest.raises(HTTPException) as e:
        main.predict(payload=payload, db=None)

    assert e.value.status_code == 400
    assert "Invalid input for model" in e.value.detail


@pytest.mark.unit
def test_generic_exception_becomes_500(mock_model_factory):
    from app import main
    mock_model_factory(raise_exc=RuntimeError("boom"))

    payload = make_payload_obj()

    with pytest.raises(HTTPException) as e:
        main.predict(payload=payload, db=None)

    assert e.value.status_code == 500
    assert "Internal error" in e.value.detail


