from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

class LikeRequest(BaseModel):
    userId: int

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

# Endpoint pour récupérer toutes les vidéos
@app.route("/getVideos", methods=["GET"])
def get_videos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Récupérer les vidéos
        cursor.execute("SELECT * FROM islamic_content")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6000)
