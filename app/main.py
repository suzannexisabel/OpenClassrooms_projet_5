from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd

from app.schemas import PredictRequest, PredictResponse
from app.model import load_model

app = FastAPI(
    title="ML Model API",
    description="API FastAPI pour exposer un pipline (preprocessor + RandomForestClassifier) de scikit-learn :" \
    "Permettant de détecter les employés qui sont succeptible de quitter l'entreprise",
    version="1.0.0"
)

@app.get("/health")
def health():
    """
    Endpoint pour verrifier que l'API fonctionne et que le modele est chargeable.
    """
    try:
        pipline = load_model()
        return {'status': 'ok', 'model_loaded': pipline is not None}
    except Exception as e:
        return {'status': 'error', 'derail': str(e)}

# Seuil métié fixé pour notre projet  
THRESHOLD = 0.47 

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    """
    Endpoint de prédiction.
    
    - payload: JSON validé par Pydantic (PredictRequest)
    - Conversion en DataFrame avec les bons noms de colonnes
    - Prédiction via pipeline.predict()
    """
    try:
        pipeline = load_model()

        # by_alias=True pour produire "Célibataire" au lieu de "celibataire"
        row = payload.model_dump(by_alias=True)

        # Dataframe
        df = pd.DataFrame([row])

        # Probabilité de chaque classe
        proba = pipeline.predict_proba(df)[0]

        # Inddex de la classe positive (1)
        classes = list(pipeline.classes_)
        positive_class_index = classes.index(1)

        # probalilité de la classe positive 
        proba_positive = float(proba[positive_class_index])

        # application du seuil métier 
        prediction = int(proba_positive >= THRESHOLD) 

        return PredictResponse(prediction=prediction, probability=proba_positive)
    
    except ValueError as e:
        # Erreurs de type : colonne manquante, mauvais type, etc.
        raise HTTPException(status_code=400, detail=f"Invalid input for model: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
