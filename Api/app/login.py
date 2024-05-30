from flask import Flask, request, jsonify
import pyodbc

def obtener_usuarios():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT [user], [password] FROM tb_user')
    usuarios = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    data = [{'id': row[0], 'name': row[1]} for row in usuarios]

    return jsonify(data)

def obtener_user(user, password):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    query = f"""
    SELECT CASE 
        WHEN EXISTS (SELECT 1 FROM tb_user WHERE [user] = '{user}' AND [password] = '{password}') 
        THEN CAST(1 AS BIT) 
        ELSE CAST(0 AS BIT) 
    END AS Existe
    """
    cursor.execute(query)
    resultado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    existe = resultado[0] if resultado else 0

    return jsonify(existe)

def crear_user(name, lastname, user, password, level):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-58K8SPAP\\SQLEXPRESS;'
        'DATABASE=MovieReviewDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    query = f"""
            insert into tb_user([name],  lastname, [user], [password], [level], createdate)
              values('{name}', '{lastname}', '{user}', '{password}', {level}, GETDATE())
            """
    
    try:
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        return False
