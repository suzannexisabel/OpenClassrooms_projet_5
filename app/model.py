from pathlib import Path
import joblib 
from huggingface_hub import hf_hub_download
import os

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "model.joblib"

_model = None

def load_model():
    """Charge le modèle en donnant la priorité au fichier local (models/model.joblib).
    Si le fichier local n'existe pas, tente de télécharger depuis HF (token requis)."""
    global _model
    if _model is not None:
        return _model
    
    # Si le modele existe en local, on le charge directement
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)
        return _model
    
    # Sinon, tente de le télécharger depuis HF hub
    token= os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "Aucun modèle local trouvé et aucun token HF fourni. "
            "En local, ajoute 'models/model.joblib' ou définis HF_TOKEN. "
            "Dans Hugging Face Space : Settings → Variables and secrets → HF_TOKEN."
        )
    
     # hf_hub_download retourne le chemin vers le cache local
    model_path = hf_hub_download(
        repo_id="suzannexisabel/HF_model_OC_projet_5",
        filename="model.joblib",
        token=token,
    )
    
    _model = joblib.load(model_path)
    return _model





