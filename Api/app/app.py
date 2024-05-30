from flask import Flask, request, jsonify

from movies import obtener_peliculas
from login import crear_user, obtener_user, obtener_usuarios
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/register', methods=["POST"])
def post_new_user():
    datos = request.get_json()
    
    name = datos.get('name')
    lastname = datos.get('lastname')
    user = datos.get('user')
    password = datos.get('password')
    level = datos.get('level')

    success = crear_user(name, lastname, user, password, level)
    if success:
        return jsonify({"Mensaje": "Usuario creado correctamente"}), 201
    else:
        return jsonify({"error": "Server error"}), 500

@app.route('/api/login', methods=["POST"])
def login():
    datos = request.get_json()

    user = datos.get('user')
    password = datos.get('password')

    user_exist = obtener_user(user, password)

    return user_exist

@app.route('/api/allusers', methods=["GET"])
def get_users():
    usuarios = obtener_usuarios()
    return usuarios

@app.route('/api/allmovies', methods=["GET"])
def get_movies():
    movies = obtener_peliculas()
    return movies

if __name__ == '__main__':
    app.run(debug=True)
