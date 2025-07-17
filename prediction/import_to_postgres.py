import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# 🔁 Εδώ βάζεις το CSV που θέλεις να φορτώσεις
csv_path = "D:/arxeia_csv2/hlorofylli_2014_2019_SP_Chla2.csv"

# Διαβάζουμε το CSV
df = pd.read_csv(csv_path, delimiter=';')

# ✅ Μετατροπή όλων των ονομάτων στηλών σε πεζά
df.columns = df.columns.str.lower()

# Στήλες του πίνακα στο PostgreSQL
required_columns = [
    "imerominia", "station", "latitude", "longitude",
    "depsm", "tv290c", "sal00", "conductivity_s_per_m",
    "secchi_depth_m", "ph", "dissolved_oxygen_pct", "dissolved_oxygen_mgl",
    "chla_ugl", "chla_rfu"
]

# Προσθέτουμε όποιες στήλες λείπουν με None
for col in required_columns:
    if col not in df.columns:
        df[col] = None

# Κρατάμε μόνο τις στήλες που θέλουμε, με σωστή σειρά
df = df[required_columns]

# Αντικατάσταση "," με "." και μετατροπή 'None' σε np.nan
for col in df.columns:
    if df[col].dtype == object:
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False).replace("None", np.nan).replace("nan", np.nan)

# Μετατροπή αριθμητικών στηλών σε float
numeric_cols = [
    "latitude", "longitude", "depsm", "tv290c", "sal00", "conductivity_s_per_m",
    "secchi_depth_m", "ph", "dissolved_oxygen_pct", "dissolved_oxygen_mgl",
    "chla_ugl", "chla_rfu"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Μετατροπή imerominia σε έγκυρη ημερομηνία
df["imerominia"] = pd.to_datetime(df["imerominia"] + "-01", errors='coerce')

# Σύνδεση με PostgreSQL
db_url = "postgresql://postgres:postgresthomasPapsterg*@localhost:5432/basiEkpaideusis"
engine = create_engine(db_url)

# Εισαγωγή στη βάση
df.to_sql("metriseis_2014_2019", engine, if_exists="append", index=False)

print("✅ Εισαγωγή επιτυχής!")