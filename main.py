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

# Vidéos d'un utilisateur
@app.route("/getUserVideos/user/<int:user_id>")
def get_user_videos(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `islamic_content` WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(results)
    except mysql.connector.Error as e:
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

# Nombre de vidéos + IDs par utilisateur
@app.route("/user/<int:user_id>/video_count", methods=["GET"])
def count_user_videos(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM islamic_content WHERE user_id = %s", (user_id,))
        results = cursor.fetchall()
        conn.close()

        if results:
            video_ids = [video['id'] for video in results]
            return jsonify({
                "user_id": user_id,
                "total_video_count": len(video_ids),
                "video_ids": video_ids
            })
        else:
            return jsonify({"error": "Utilisateur non trouvé ou aucune vidéo disponible"}), 404
    except mysql.connector.Error as e:
        return jsonify({"error": f"Erreur lors de la connexion à la base de données: {str(e)}"}), 500

# Like / Dislike
@app.route("/content/<int:content_id>/like", methods=["POST"])
def toggle_like(content_id):
    user_id = request.json.get("userId")
    if not user_id:
        return jsonify({"error": "L'ID utilisateur est requis"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND content_id = %s)", (user_id, content_id))
    (has_liked,) = cursor.fetchone()

    if has_liked:
        cursor.execute("DELETE FROM likes WHERE user_id = %s AND content_id = %s", (user_id, content_id))
        response = {"liked": False}
    else:
        cursor.execute("INSERT INTO likes (user_id, content_id) VALUES (%s, %s)", (user_id, content_id))
        response = {"liked": True}

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(response)

# Nombre de likes
@app.route("/content/<int:content_id>/likes", methods=["GET"])
def get_likes(content_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM likes WHERE content_id = %s", (content_id,))
    (count,) = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"count": count})

# -------------------- Upload OVH --------------------

def get_ovh_connection():
    return swiftclient.Connection(
        user='user-RAqDwcWqKbhS',
        key='k2EsKaGyy3BC3xDRrVmXhsspNCrw74uN',
        authurl='https://auth.cloud.ovh.net/v3',
        os_options={
            'project_id': '2b45951fb19c42d197be8ee756932ff1',
            'user_id': 'ccabed683df844d9aebb49b9a7eaaba7',
            'region_name': 'GRA'
        },
        auth_version='3'
    )

@app.route("/upload", methods=["POST"])
def upload():
    print("Files received:", request.files)

    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    filename = file.filename
    content = file.read()

    try:
        conn = get_ovh_connection()
        container = "Muslim.Vibes/Videos"
        conn.put_object(container, filename, contents=content)
        return jsonify({"message": f"Fichier {filename} envoyé avec succès à OVH."})
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'upload: {str(e)}"}), 500

# -------------------- Run --------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
