import pytest
from pydantic import ValidationError

from app.schemas import PredictRequest

@pytest.mark.unit
def test_pydantic_validation_is_enforced_before_predict():
    # exemple: age < 18 => validation error
    with pytest.raises(ValidationError):
        PredictRequest(
            age=17,
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