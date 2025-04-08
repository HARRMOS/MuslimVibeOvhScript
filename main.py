from flask import Flask, jsonify, request
import mysql.connector
import swiftclient

app = Flask(__name__)

# -------------------- Base de Données --------------------

def get_db_connection():
    return mysql.connector.connect(
        host="mh285989-001.eu.clouddb.ovh.net",
        port=35693,
        user="bts",
        password="Harris91270",
        database="MuslimVibe"
    )
@app.route("/")
def home():
    return "✅ L'application Flask fonctionne !"
# Route pour récupérer toutes les vidéos
@app.route("/getVideos")
def get_videos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `islamic_content`")
        results = cursor.fetchall()
        conn.close()
        return jsonify(results)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500
