import sqlite3
import csv

# Σύνδεση με βάση
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Άνοιγμα αρχείου με σωστό delimiter (;)
with open("KENTRIKIS_MAKEDONIAS_AUGOUSTOS_2023.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        cursor.execute("""
        INSERT INTO metriseis (
            bwid, imerominia, conc_ec, conc_ie, wind_direction,
            other_pollution, tar_residue, glasses, plastics,
            rubber, other_waste, presence_of_algae, presence_of_oil
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['\ufeffbwid'],  # διορθωμένο για BOM
            row['imerominia'],
            int(row['conc_ec']),
            int(row['conc_ie']),
            row['wind_direction'],
            row['other_pollution'],
            row['tar_residue'],
            row['glasses'],
            row['plastics'],
            row['rubber'],
            row['other_waste'],
            row['presence_of_aglae'],
            row['presence_of_oil']
        ))

conn.commit()
conn.close()

print("✅ Οι μετρήσεις εισήχθησαν με επιτυχία.")
