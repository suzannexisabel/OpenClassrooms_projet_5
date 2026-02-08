from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class PredictRequest(BaseModel):
    # acceptation des noms de colonnes Python et produire les noms dataset (alias)
    model_config = ConfigDict(populate_by_name=True)

    # Numériques (int)
    age: int = Field(..., ge=18, le=60, description="Age de l'employé")
    nombre_experiences_precedentes: int = Field(..., ge=0, le=9, description="Nombre d'expériences précédentes")
    niveau_hierarchique_poste: int = Field(..., ge=1, le=5, description='hierarchie 1 : bas, hierarchie 5 : haut')
    heure_supplementaires: int = Field(..., ge=0, le=1, description='0=aucune, 1=oui')
    nombre_participation_pee: int = Field(..., ge=0, le=3, description='participation pee')
    niveau_education: int = Field(..., ge=1, le=5, description="niveau education")
    frequence_deplacement_code: int = Field(..., ge=1, le=3, description='1=faible, 2=moyen, 3=élevé')
    delta_evaluation: int = Field(..., ge=-1, le=3, description="Points d'écarts entre la dernière évaluation")
    annees_dans_l_entreprise_bins: int = Field(..., ge=0, le=4, description="0=")
    distance_domicile_travail_bins: int = Field(..., ge=0, le=2, description="0=")
    celibataire: int = Field(..., ge=0, le=1, alias="Célibataire", description= "0=non, 1=oui")

    # Numériques (Float)
    ratio_anciennete_manager: float = Field(..., ge=0.0, le=1.0, description="pourcentage sous responsable actuel / temps dans l'entreprise")
    score_satisfaction_global: float = Field(..., ge=1.0, le=4.4, description="Moyenne des différentes satisfactions")

    # Catégorielles 
    genre: Literal["F", "M"]
    poste: Literal[
        "Assistant de Direction",
        "Cadre Commercial",
        "Consultant",
        "Directeur Technique",
        "Manager",
        "Représentant Commercial",
        "Ressources Humaines",
        "Senior Manager",
        "Tech Lead",
    ]
    domaine_etude: Literal[
        "Autre",
        "Entrepreunariat",
        "Infra & Cloud",
        "Marketing",
        "Ressources Humaines",
        "Transformation Digitale",
    ]

class PredictResponse(BaseModel):
    prediction: int
    probability: float | None = None


