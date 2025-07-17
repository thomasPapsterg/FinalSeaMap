import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import SimpleImputer
import joblib
import os

# --- Σύνδεση με PostgreSQL ---
db_url = "postgresql://postgres:postgresthomasPapsterg*@localhost:5432/basiEkpaideusis"
engine = create_engine(db_url)

# --- Διαβάζουμε τα δεδομένα ---
df = pd.read_sql("SELECT * FROM metriseis_2014_2019", engine)
df = df.dropna(subset=['sal00'])  # αφαιρεί μόνο όσα δεν έχουν sal00

# --- Επιλογή χαρακτηριστικών και στόχου ---
X = df[['depsm', 'tv290c', 'conductivity_s_per_m', 'secchi_depth_m',
        'ph', 'dissolved_oxygen_pct', 'dissolved_oxygen_mgl']]
y = df['sal00']

# --- Αντικατάσταση NaN με μέση τιμή ---
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# --- Εκπαίδευση ή φόρτωση μοντέλου ---
model_path = "salinity_model.pkl"
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print(" Το μοντέλο φορτώθηκε από το αρχείο.")
else:
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
    print(" Το μοντέλο εκπαιδεύτηκε και αποθηκεύτηκε.")

    # --- Αξιολόγηση ---
    y_pred = model.predict(X_test)
    print("R² score:", round(r2_score(y_test, y_pred), 3))
    print("MSE:", round(mean_squared_error(y_test, y_pred), 3))

    # --- Οπτικοποίηση ---
    plt.scatter(y_test, y_pred)
    plt.xlabel("Πραγματικές Τιμές Αλατότητας")
    plt.ylabel("Προβλεπόμενες Τιμές Αλατότητας")
    plt.title("Πραγματικές vs Προβλεπόμενες")
    plt.grid(True)
    plt.show()

# --- Πρόβλεψη με είσοδο χρήστη ---
print("\n📌 Δώσε τιμές για να γίνει πρόβλεψη αλατότητας:")
depth = float(input("Βάθος (m): "))
temp = float(input("Θερμοκρασία (°C): "))
conductivity = float(input("Αγωγιμότητα (S/m): "))
secchi = float(input("Βάθος δίσκου Secchi (m): "))
ph = float(input("pH: "))
oxygen_pct = float(input("Οξυγόνο %: "))
oxygen_mgl = float(input("Οξυγόνο (mg/L): "))

user_data = pd.DataFrame([[depth, temp, conductivity, secchi, ph, oxygen_pct, oxygen_mgl]],
                         columns=X.columns)

# Προεπεξεργασία όπως στο training
user_data_imputed = imputer.transform(user_data)

# Πρόβλεψη
pred = model.predict(user_data_imputed)[0]
print(f"\n📍 Προβλεπόμενη Αλατότητα: {round(pred, 2)} PSU")

# --- Επιβεβαίωση ότι το μοντέλο αποθηκεύτηκε και φορτώνεται σωστά ---
model_test = joblib.load("salinity_model.pkl")
print("✅ Το αποθηκευμένο μοντέλο φορτώθηκε:", type(model_test))