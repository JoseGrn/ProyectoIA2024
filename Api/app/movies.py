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
    cursor.execute('SELECT movieid,[rotten_tomatoes_link], [movie_title], movie_info, genres, directors, authors, actors, original_release_date, streaming_release_date, runtime, production_company FROM tb_movie')
    movies = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    data = [{'id': row[0], 'link': row[1], 'titulo': row[2], 'informacion': row[3], 'generos': row[4], 'directores': row[5], 'autores': row[6], 'actores': row[7], 'FechaEstreno': row[8], 'FechaStreaming': row[9], 'duracion': row[10], 'productora': row[11]} for row in movies]

    return jsonify(data)

def do_review(userid, movieid, score, comment):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    tomatometer = "Fresh"
    query = f"""
            insert into tb_review([userid],[movieid],[score],[comment],[reviewdate],[tomatometer])
            values({userid}, {movieid}, {score}, '{comment}', GETDATE(), '{tomatometer}')
            """
    
    try:
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return False