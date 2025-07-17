import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metriseis (
  bwid TEXT,
  imerominia TEXT,
  conc_ec INTEGER,
  conc_ie INTEGER,
  wind_direction TEXT,
  other_pollution TEXT,
  tar_residue TEXT,
  glasses TEXT,
  plastics TEXT,
  rubber TEXT,
  other_waste TEXT,
  presence_of_algae TEXT,
  presence_of_oil TEXT
)
""")

# Δημιουργία πίνακα παραλιών με όνομα και bwid
cursor.execute("""
CREATE TABLE IF NOT EXISTS beaches (
    name TEXT,
    bwid TEXT PRIMARY KEY
)
""")

# Εισαγωγή ενδεικτικών δεδομένων
cursor.executemany("""
INSERT OR REPLACE INTO beaches (name, bwid) VALUES (?, ?)
""", [
    ("Καλαμαριά", "ELBW089046031101"),
    ("Περαία", "ELBW089046031201"),
    ("Αγία Τριάδα", "ELBW109029022101")
])

cursor.execute("""
INSERT INTO metriseis VALUES (
  'ELBW089046031101', '2023-08-13', 4, 2, 'ΒΑ', 'ΟΧΙ', 'ΌΧΙ', 'Όχι', 'Όχι', 'Όχι', 'Όχι', 'ΟΧΙ', 'ΟΧΙ'
)
""")

conn.commit()
conn.close()
