import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Σύνδεση με PostgreSQL
db_url = "postgresql://postgres:postgresthomasPapsterg*@localhost:5432/basiEkpaideusis"
engine = create_engine(db_url)

# Ανάγνωση δεδομένων
query = "SELECT * FROM metriseis_2014_2019"
df = pd.read_sql(query, engine)

# Αφαίρεση γραμμών με NaN στη μεταβλητή στόχο
df = df.dropna(subset=['sal00'])

# Εισαγωγή χαρακτηριστικών εισόδου (X) και στόχου (y)
X = df[['depsm', 'tv290c', 'conductivity_s_per_m', 
        'secchi_depth_m', 'ph', 'dissolved_oxygen_pct', 'dissolved_oxygen_mgl']]

y = df['sal00']

# Μετατροπή σε αριθμούς και NaN -> μέση τιμή
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(X.mean())

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Διαχωρισμός
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Μοντέλο
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Πρόβλεψη και αξιολόγηση
y_pred = model.predict(X_test)

print("R² score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))


plt.scatter(y_test, y_pred)
plt.xlabel("Πραγματικές Τιμές chla_ugl")
plt.ylabel("Προβλεπόμενες Τιμές chla_ugl")
plt.title("Πραγματικές vs Προβλεπόμενες")
plt.grid(True)
plt.show()