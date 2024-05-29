from flask import Flask, request, jsonify
import pyodbc

def obtener_usuarios():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT [user], [password] FROM tb_user')
    usuarios = cursor.fetchall()
    conn.close()

    data = [{'id': row[0], 'name': row[1]} for row in usuarios]

    return jsonify(data)
