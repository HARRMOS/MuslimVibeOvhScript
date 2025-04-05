from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/getVideos")
def get_videos():
    conn = mysql.connector.connect(
        host="mh285989-001.eu.clouddb.ovh.net",
        user="bts",
        password="Harris91270",
        database="MuslimVibe"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM `MuslimVibe`")
    results = cursor.fetchall()
    conn.close()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
