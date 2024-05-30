from flask import Flask, request, jsonify
import pyodbc

def obtener_peliculas():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT [rotten_tomatoes_link], [movie_title] FROM tb_movie')
    movies = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    data = [{'link': row[0], 'title': row[1]} for row in movies]

    return jsonify(data)