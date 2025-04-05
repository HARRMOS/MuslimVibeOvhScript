from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/getVideos")
def get_videos():
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,  # Spécifier le port ici
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)
        
        # Exécuter la requête SQL
        cursor.execute("SELECT * FROM `islamic_content`")  # Remplace `MuslimVibe` par le nom de ta table si nécessaire
        results = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()

        # Retourner les résultats sous forme de JSON
        return jsonify(results)
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="0.0.0.0", port=6000)
