from flask import Flask, request, jsonify

from GeneratePerceptron import SentimentModel
from movies import commentByMovie, commentByUser, do_review, getallreviews, obtener_peliculas
from login import crear_user, obtener_user, obtener_usuarios
from flask_cors import CORS

app = Flask(__name__)

sentiment_model = SentimentModel(38000)
history = sentiment_model.train('C:/Users/josed/Downloads/rotten_tomatoes_critic_reviews_p.csv')

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

@app.route('/api/review', methods=["POST"])
def review():
    datos = request.get_json()
    
    userid = datos.get('userid')
    movieid = datos.get('movieid')
    score = datos.get('score')
    comment = datos.get('comment')

    prediccion = sentiment_model.predict_review(comment)

    success = do_review(userid, movieid, score, comment, prediccion)
    
    if success:
        return jsonify({"Mensaje": "Review creada correctamente"}), 201
    else:
        return jsonify({"error": "Server error"}), 500
    
@app.route('/api/reviewbyuser', methods=["POST"])
def reviewByUser():
    datos = request.get_json()
    
    userid = datos.get('userid')

    comentarios = commentByUser(userid)
    
    return comentarios

@app.route('/api/reviewbymovie', methods=["POST"])
def reviewByMovie():
    datos = request.get_json()
    
    movieid = datos.get('movieid')

    comentarios = commentByMovie(movieid)
    
    return comentarios

@app.route('/api/allreviews', methods=["GET"])
def allreviews():
    comentarios = getallreviews()
    return comentarios

@app.route('/api/allmovies', methods=["GET"])
def get_movies():
    movies = obtener_peliculas()
    return movies

if __name__ == '__main__':
    app.run(debug=True)
