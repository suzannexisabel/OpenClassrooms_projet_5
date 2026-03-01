import os
from sqlalchemy import create_engine, text

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set (local .env)")

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    queries = {
        "n_predictions": "SELECT COUNT(*) FROM app.prediction_result;",
        "avg_latency_ms": "SELECT AVG(latency_ms) FROM app.prediction_result;",
        "avg_proba_positive": "SELECT AVG(proba_positive) FROM app.prediction_result;",
        "dataset_rows": "SELECT COUNT(*) FROM app.employee_dataset;",
    }

    with engine.connect() as conn:
        for name, q in queries.items():
            val = conn.execute(text(q)).scalar()
            print(f"{name}: {val}")

if __name__ == "__main__":
    main()