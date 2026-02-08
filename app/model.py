from pathlib import Path
import joblib 
from huggingface_hub import hf_hub_download

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.joblib"

_model = None

def load_model():
    global _model
    if _model is not None:
        return _model
    
    if not MODEL_PATH.exists():
        _download_model()


    _model = joblib.load(MODEL_PATH)
    return _model

def _download_model():
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    downloaded_path = hf_hub_download(
        repo_id="suzannexisabel/HF_model_OC_projet_5",
        filename="model.joblib"
    )

    # Copie du cache HF vers models/
    MODEL_PATH.write_bytes(Path(downloaded_path).read_bytes())




