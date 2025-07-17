import sqlite3
import csv

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS beaches (
    bwid TEXT PRIMARY KEY,
    name TEXT
)
""")

with open("names-of-beaches.csv", newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')  # ΔΙΟΡΘΩΜΕΝΟ delimiter και BOM
    for row in reader:
        try:
            bwid = row['bwid'].strip()
            name = row['name'].strip()
            cursor.execute("""
                INSERT OR REPLACE INTO beaches (bwid, name)
                VALUES (?, ?)
            """, (bwid, name))
        except Exception as e:
            print(f"❌ Σφάλμα στην παραλία {row.get('name', '?')}: {e}")

conn.commit()
conn.close()
print("✅ Οι παραλίες εισήχθησαν με επιτυχία.")



