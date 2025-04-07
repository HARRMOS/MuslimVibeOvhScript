from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Route pour récupérer toutes les vidéos
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
        
        # Exécuter la requête SQL pour récupérer toutes les vidéos
        cursor.execute("SELECT * FROM `islamic_content`")
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
            port=35693,
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)
        
        # Exécuter la requête SQL pour obtenir le nombre de vidéos par utilisateur
        cursor.execute("""
             SELECT video_id, COUNT(*) AS video_count 
            FROM islamic_content 
            WHERE user_id = %s
            GROUP BY video_id
        """, (user_id,))
        
       # Récupérer les résultats
        results = cursor.fetchall()
        
        # Fermer la connexion
        conn.close()

        # Vérifier si des vidéos ont été trouvées pour l'utilisateur
        if results:
            return jsonify({"user_id": user_id, "videos": results})
        else:
            return jsonify({"error": "Utilisateur non trouvé ou aucune vidéo disponible"}), 404
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500


# Route pour "liker" une vidéo
@app.route("/like", methods=["POST"])
def like_video():
    data = request.json
    user_id = data.get("user_id")
    video_id = data.get("video_id")
    
    if not user_id or not video_id:
        return jsonify({"error": "user_id et video_id sont requis"}), 400
    
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour insérer un like
        cursor = conn.cursor()
        
        # Vérifier si le like existe déjà
        cursor.execute("""
            SELECT * FROM video_likes 
            WHERE user_id = %s AND video_id = %s
        """, (user_id, video_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            return jsonify({"error": "Vous avez déjà liké cette vidéo"}), 400
        
        # Insérer un nouveau like
        cursor.execute("""
            INSERT INTO video_likes (user_id, video_id) 
            VALUES (%s, %s)
        """, (user_id, video_id))
        conn.commit()

        # Fermer la connexion
        conn.close()

        return jsonify({"message": "Like ajouté avec succès"}), 201
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500


# Route pour récupérer le nombre de likes d'une vidéo
@app.route("/video/<int:video_id>/like_count", methods=["GET"])
def get_like_count(video_id):
    try:
        # Connexion à la base de données
        conn = mysql.connector.connect(
            host="mh285989-001.eu.clouddb.ovh.net",
            port=35693,
            user="bts",
            password="Harris91270",
            database="MuslimVibe"
        )

        # Créer un curseur pour interroger la base de données
        cursor = conn.cursor(dictionary=True)
        
        # Exécuter la requête SQL pour obtenir le nombre de likes pour la vidéo
        cursor.execute("""
            SELECT COUNT(*) AS like_count 
            FROM video_likes 
            WHERE video_id = %s
        """, (video_id,))
        
        # Récupérer le résultat
        result = cursor.fetchone()
        
        # Fermer la connexion
        conn.close()

        # Retourner le nombre de likes
        if result:
            return jsonify({"video_id": video_id, "like_count": result["like_count"]})
        else:
            return jsonify({"error": "Aucun like trouvé pour cette vidéo"}), 404
    
    except mysql.connector.Error as e:
        # Gestion des erreurs de connexion
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500


if __name__ == "__main__":
    # Lancer l'application Flask
    app.run(debug=True, host="0.0.0.0", port=6000)
