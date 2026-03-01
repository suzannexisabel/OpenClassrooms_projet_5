import os
import pandas as pd
from sqlalchemy import create_engine, text

from dotenv import load_dotenv
load_dotenv()

CSV_PATH = os.getenv("DATASET_PATH", "data/employee_churn_dataset_for_db.csv")
DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set (check your .env)")

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # (Optionnel) sécurise les colonnes attendues
    expected_cols = [
        "age",
        "genre",
        "poste",
        "nombre_experiences_precedentes",
        "niveau_hierarchique_poste",
        "heure_supplementaires",
        "a_quitte_l_entreprise",
        "nombre_participation_pee",
        "niveau_education",
        "domaine_etude",
        "ratio_anciennete_manager",
        "frequence_deplacement_code",
        "score_satisfaction_global",
        "delta_evaluation",
        "Célibataire",
        "annees_dans_l_entreprise_bins",
        "distance_domicile_travail_bins",
    ]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")

    # Casts (pour éviter les surprises)
    int_cols = [
        "age",
        "nombre_experiences_precedentes",
        "niveau_hierarchique_poste",
        "heure_supplementaires",
        "a_quitte_l_entreprise",
        "nombre_participation_pee",
        "niveau_education",
        "frequence_deplacement_code",
        "delta_evaluation",
        "Célibataire",
        "annees_dans_l_entreprise_bins",
        "distance_domicile_travail_bins",
    ]
    float_cols = ["ratio_anciennete_manager", "score_satisfaction_global"]

    for c in int_cols:
        df[c] = df[c].astype(int)

    for c in float_cols:
        df[c] = df[c].astype(float)

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

    insert_sql = text("""
        INSERT INTO app.employee_dataset (
          age, genre, poste, nombre_experiences_precedentes,
          niveau_hierarchique_poste, heure_supplementaires,
          a_quitte_l_entreprise, nombre_participation_pee,
          niveau_education, domaine_etude, ratio_anciennete_manager,
          frequence_deplacement_code, score_satisfaction_global,
          delta_evaluation, "Célibataire",
          annees_dans_l_entreprise_bins, distance_domicile_travail_bins
        )
        VALUES (
          :age, :genre, :poste, :nombre_experiences_precedentes,
          :niveau_hierarchique_poste, :heure_supplementaires,
          :a_quitte_l_entreprise, :nombre_participation_pee,
          :niveau_education, :domaine_etude, :ratio_anciennete_manager,
          :frequence_deplacement_code, :score_satisfaction_global,
          :delta_evaluation, :celibataire,
          :annees_dans_l_entreprise_bins, :distance_domicile_travail_bins
        )
    """)

    with engine.begin() as conn:
        # Optionnel : réimport propre (décommente si tu veux toujours repartir de zéro)
        # conn.execute(text("TRUNCATE TABLE app.employee_dataset RESTART IDENTITY;"))

        rows = df.to_dict(orient="records")
        # Adapter la clé pour le paramètre :celibataire (sans accent)
        for r in rows:
            r["celibataire"] = r.pop("Célibataire")

        conn.execute(insert_sql, rows)

    print(f"Imported {len(df)} rows into app.employee_dataset from {CSV_PATH}")

if __name__ == "__main__":
    main()