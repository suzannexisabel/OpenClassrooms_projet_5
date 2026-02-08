from pathlib import Path
import joblib 

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.joblib"

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


