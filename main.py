from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Endpoint pour liker / déliker
@app.post("/content/{content_id}/like")
async def toggle_like(content_id: int, request: LikeRequest):
    async with app.state.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND content_id = %s)",
                (request.userId, content_id)
            )
            (has_liked,) = await cur.fetchone()

            if has_liked:
                await cur.execute(
                    "DELETE FROM likes WHERE user_id = %s AND content_id = %s",
                    (request.userId, content_id)
                )
                await conn.commit()
                return {"liked": False}
            else:
                await cur.execute(
                    "INSERT INTO likes (user_id, content_id) VALUES (%s, %s)",
                    (request.userId, content_id)
                )
                await conn.commit()
                return {"liked": True}

# Endpoint pour obtenir le nombre de likes
@app.get("/content/{content_id}/likes")
async def get_likes(content_id: int):
    async with app.state.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) FROM likes WHERE content_id = %s",
                (content_id,)
            )
            (count,) = await cur.fetchone()
            return {"count": count}


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
