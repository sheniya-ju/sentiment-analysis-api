import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sheju2498",
        database="sentiment_db"
    )

def save_prediction(text, sentiment, confidence):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (input_text, sentiment, confidence) VALUES (%s, %s, %s)",
        (text, sentiment, confidence)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_predictions():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results