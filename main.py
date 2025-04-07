from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    return mysql.connector.connect(
        host="mh285989-001.eu.clouddb.ovh.net",
        port=35693,
        user="bts",
        password="Harris91270",
        database="MuslimVibe"
    )

# Endpoint pour liker / déliker
@app.route("/content/<int:content_id>/like", methods=["POST"])
def toggle_like(content_id):
    user_id = request.json.get("userId")
    if not user_id:
        return jsonify({"error": "L'ID utilisateur est requis"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si l'utilisateur a déjà liké
    cursor.execute(
        "SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND content_id = %s)",
        (user_id, content_id)
    )
    (has_liked,) = cursor.fetchone()

    if has_liked:
        cursor.execute(
            "DELETE FROM likes WHERE user_id = %s AND content_id = %s",
            (user_id, content_id)
        )
        conn.commit()
        response = {"liked": False}
    else:
        cursor.execute(
            "INSERT INTO likes (user_id, content_id) VALUES (%s, %s)",
            (user_id, content_id)
        )
        conn.commit()
        response = {"liked": True}

    cursor.close()
    conn.close()
    return jsonify(response)

# Endpoint pour obtenir le nombre de likes
@app.route("/content/<int:content_id>/likes", methods=["GET"])
def get_likes(content_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer le nombre de likes
    cursor.execute(
        "SELECT COUNT(*) FROM likes WHERE content_id = %s",
        (content_id,)
    )
    (count,) = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return jsonify({"count": count})

from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

class LikeRequest(BaseModel):
    userId: int

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


# Route pour récupérer le nombre de vidéos par utilisateur
@app.route("/user/<int:user_id>/video_count", methods=["GET"])
def get_video_count(user_id):
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
        
        # Exécuter la requête SQL pour obtenir le nombre de vidéos par utilisateur
        cursor.execute("""
            SELECT COUNT(*) AS video_count 
            FROM islamic_content 
            WHERE user_id = %s
        """, (user_id,))
        
        # Récupérer le résultat
        result = cursor.fetchone()
        
        # Fermer la connexion
        conn.close()

        # Vérifier si des vidéos ont été trouvées pour l'utilisateur
        if result:
            return jsonify({"user_id": user_id, "video_count": result["video_count"]})
        else:
            return jsonify({"error": "Utilisateur non trouvé ou aucune vidéo disponible"}), 404
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="0.0.0.0", port=6000)
