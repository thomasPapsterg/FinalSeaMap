import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("""
SELECT DISTINCT beaches.name, beaches.bwid
FROM beaches
JOIN metriseis ON beaches.bwid = metriseis.bwid
""")

results = cursor.fetchall()
conn.close()

if results:
    print("✅ Παραλίες με διαθέσιμες μετρήσεις:\n")
    for name, bwid in results:
        print(f"- {name} ({bwid})")
else:
    print("⚠️ Δεν υπάρχουν παραλίες με διαθέσιμες μετρήσεις.")
