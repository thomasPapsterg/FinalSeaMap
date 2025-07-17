from flask_cors import CORS
from flask import Flask, request, jsonify
import sqlite3
import unicodedata

app = Flask(__name__)
CORS(app)

# 🔣 Αφαίρεση τόνων από ελληνικά (π.χ. Καλαμαριά → Καλαμαρια)
def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

# 🔍 Δεδομένα παραλίας με βάση BWID
def get_beach_data(bwid):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT conc_ec, conc_ie, wind_direction, other_pollution, tar_residue,
               glasses, plastics, rubber, other_waste,
               presence_of_algae, presence_of_oil
        FROM metriseis
        WHERE bwid = ?
        ORDER BY imerominia DESC
        LIMIT 1
    """, (bwid,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        fields = [
            "conc_ec", "conc_ie", "wind_direction", "other_pollution", "tar_residue",
            "glasses", "plastics", "rubber", "other_waste",
            "presence_of_algae", "presence_of_oil"
        ]
        return dict(zip(fields, row))
    return None

# 📡 Εύρεση BWID βάσει ονόματος παραλίας
@app.route('/get_bwid', methods=['GET'])
def get_bwid():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "Δώσε όνομα παραλίας."}), 400

    name_normalized = remove_accents(name.lower())

    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, bwid FROM beaches")
    all_rows = cursor.fetchall()
    conn.close()

    for db_name, db_bwid in all_rows:
        db_name_normalized = remove_accents(db_name.lower())
        if name_normalized in db_name_normalized:
            return jsonify({"bwid": db_bwid})

    return jsonify({"error": "Δεν βρέθηκε παραλία με αυτό το όνομα."}), 404

# 📡 Επιστροφή δεδομένων βάσει BWID
@app.route('/get_data', methods=['GET'])
def get_data():
    bwid = request.args.get('bwid')
    if not bwid:
        return jsonify({"error": "Παρακαλώ δώσε το bwid παραλίας."}), 400

    data = get_beach_data(bwid)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Δεν βρέθηκαν δεδομένα για την παραλία."}), 404

# 📊 Προτεινόμενες καθαρές παραλίες
@app.route('/get_best_beaches', methods=['GET'])
def get_best_beaches():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.name, m.conc_ec, m.conc_ie
        FROM metriseis m
        JOIN beaches b ON m.bwid = b.bwid
        WHERE m.conc_ec IS NOT NULL AND m.conc_ie IS NOT NULL
        GROUP BY m.bwid
        ORDER BY CAST(m.conc_ec AS REAL) + CAST(m.conc_ie AS REAL) ASC
        LIMIT 5
    """)

    results = cursor.fetchall()
    conn.close()

    return jsonify([
        {"name": row[0], "conc_ec": row[1], "conc_ie": row[2]} for row in results
    ])

# ▶️ Εκκίνηση server
if __name__ == '__main__':
    app.run(debug=True, port=5001)




