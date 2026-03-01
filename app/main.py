
import numpy as np
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import Depends

from app.schemas import PredictRequest, PredictResponse
from app.model import load_model
from app.db import get_db

import json
import time
import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session



app = FastAPI(
    title="ML Model API",
    description="API FastAPI pour exposer un pipline (preprocessor + RandomForestClassifier) de scikit-learn :" \
    "Permettant de détecter les employés qui sont succeptible de quitter l'entreprise",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body style="font-family: Arial; padding: 24px;">
        <h1>ML Model API</h1>
        <p>✅ API is running</p>
        <ul>
          <li><a href="/docs">Swagger UI</a></li>
          <li><a href="/health">Health check</a></li>
        </ul>
      </body>
    </html>
    """

@app.get("/health")
def health():
    """
    Endpoint pour verrifier que l'API fonctionne et que le modele est chargeable.
    """
    try:
        pipline = load_model()
        return {'status': 'ok', 'model_loaded': pipline is not None}
    except Exception as e:
        return {'status': 'error', 'detail': str(e)}

# Seuil métier fixer pour notre projet  
THRESHOLD = 0.47 

@app.post("/predict", 
          response_model=PredictResponse,
          summary="Prédiction de départ d'un employé",
          description="Retourne la probabilité qu'un employé quitte l'entreprise")
def predict(payload: PredictRequest, db: Session = Depends(get_db)):

    """
    Endpoint de prédiction.
    
    - payload: JSON validé par Pydantic (PredictRequest)
    - Conversion en DataFrame avec les bons noms de colonnes
    - Prédiction via pipeline.predict()
    """

    t0 = time.perf_counter()
    request_id = str(uuid.uuid4())

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
        latency_ms = int((time.perf_counter() - t0) * 1000)

        # Log de la requête
        if db is not None:
            db.execute(
                text("""
                    INSERT INTO app.prediction_request (request_id, endpoint, input_json)
                    VALUES (:request_id, :endpoint, :input_json)
                """),
                {
                    "request_id": str(request_id),
                    "endpoint": "/predict",
                    "input_json": json.dumps(row, ensure_ascii=False),
                        
                }
            )

        # ID du modele
        if db is not None:
            model_id = db.execute(
                text("""
                    SELECT id FROM app.model_registry
                    WHERE name = :name AND version = :version
                    LIMIT 1
                """),
                {"name": "employee_churn_rf", "version": "v1"}
            ).scalar_one()

            # log le résultat 
            db.execute(
                text("""
                    INSERT INTO app.prediction_result
                    (request_id, model_id, threshold, proba_positive, prediction, latency_ms)
                    VALUES
                    (:request_id, :model_id, :threshold, :proba_positive, :prediction, :latency_ms)
                """),
                {
                    "request_id": str(request_id),
                    "model_id": model_id,
                    "threshold": THRESHOLD,
                    "proba_positive": proba_positive,
                    "prediction": prediction,
                    "latency_ms": latency_ms,
                }
            )

            db.commit()

        return PredictResponse(prediction=prediction, probability=proba_positive)
    
    except ValueError as e:
        # Erreurs de type : colonne manquante, mauvais type, etc.
        raise HTTPException(status_code=400, detail=f"Invalid input for model: {str(e)}")
    except Exception as e:
        if db is not None:
            db.rollback()
        print("ERROR /predict:", repr(e))
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
