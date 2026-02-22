import sys
from pathlib import Path

import pytest 
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker


# Ajoute la racine du repo au PYTHONPATH pour que `import app...` marche
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# charge .env 
load_dotenv(ROOT / ".env")

from app.main import app
from app.db import get_db

# ----------------------------
# Dummy Pipline (model)
# ----------------------------

class DummyPipline:
    classes_ = [0,1]

    def predict_proba(self,X):
        import numpy as np
        return np.tile([0.2, 0.8], (len(X),1))
    
# ----------------------------
# Mock model
# ----------------------------

@pytest.fixture
def mock_model(monkeypatch):
    import app.main
    monkeypatch.setattr(app.main, "load_model", lambda: DummyPipline())

# ----------------------------
# Client DB OFF (mode HF)
# ----------------------------
@pytest.fixture
def client():
    # On force les test a travailler sans la db
    app.dependency_overrides[get_db] = lambda: None

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


# ----------------------------
# Engine Postgres de test (mldb_test)
# ----------------------------
@pytest.fixture(scope="session")
def test_engine():
    """Engine SQLAlchemy vers la DB de test dédiée."""
    import os

    url = os.getenv("DATABASE_URL_TEST")
    assert url, "DATABASE_URL_TEST manquant dans .env"

    engine = create_engine(url, pool_pre_ping=True)

    # init schema/tables de test dans mldb_test
    init_sql_path = ROOT / "tests" / "sql" / "init_test_db.sql"
    init_sql = init_sql_path.read_text(encoding="utf-8")
    with engine.begin() as conn:
        conn.execute(text(init_sql))

    return engine

# ----------------------------
# Nettoyage automatique DB ON
# ----------------------------
@pytest.fixture
def clean_db(test_engine):
    """
    Nettoie les tables de logs avant chaque test DB ON et remet le seed model_registry.
    (Optionnellement, re-nettoie après.)
    """
    with test_engine.begin() as conn:
        conn.execute(text("TRUNCATE app.prediction_result RESTART IDENTITY CASCADE"))
        conn.execute(text("TRUNCATE app.prediction_request RESTART IDENTITY CASCADE"))

        # seed indispensable pour /predict (sinon .scalar_one() plante)
        conn.execute(text("""
            INSERT INTO app.model_registry (name, version, artifact_path)
            VALUES ('employee_churn_rf', 'v1', 'TEST_ARTIFACT_PATH')
            ON CONFLICT (name, version) DO NOTHING
        """))

    yield

# ----------------------------
# Client DB ON (mldb_test)
# ----------------------------
@pytest.fixture
def client_with_db(test_engine, clean_db):
    """DB ON: session Postgres (mldb_test) + override Depends(get_db)."""
    TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

