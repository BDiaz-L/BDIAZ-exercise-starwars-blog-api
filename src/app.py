"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Film, Species
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Traer todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        if len(users) < 1:
            return jsonify({"msg": "Not found users"}), 404
        serialized_users = list(map( lambda x: x.serialize(), users))
        return serialized_users, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Traer solo un usuario
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"msg": f"Not found user: {user_id}"}), 404
        serialized_user = user.serialize()
        return serialized_user, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    try:
        body = json.loads(request.data)
        new_user = User(
            email = body["email"],
            password = body["password"],
            is_active = True
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User: created succefully"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Editar el usuario - extra

# Borrar el usuario - extra

# Traer todos los personajes
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        people = People.query.all()
        if len(people) < 1:
            return jsonify({"msg": "Not found people"}), 404
        serialize_people = list(map( lambda x: x.serialize(), people))
        return serialize_people, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Traer solo un personaje
@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    try:
        character = People.query.get(character_id)
        if character is None:
            return jsonify({"msg": f"Not found character: {character_id}"}), 404
        serialized_user = character.serialize()
        return serialized_user, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Crear un personaje
@app.route('/people', methods=['POST'])
def create_character():
    try:
        body = json.loads(request.data)
        new_people = People(
            name = body["name"],
            birth_year = body["birth_year"],
            eye_color = body["eye_color"],
            gender = body["gender"],
            hair_color = body["hair_color"],
            height = body["height"],
            mass = body["mass"],
            skin_color = body["skin_color"]
        )
        db.session.add(new_people)
        db.session.commit()
        return jsonify({"msg": "Character: created succefully"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Editar el personaje - extra

# Borrar el personaje - extra

# Traer todos las peliculas
@app.route('/films', methods=['GET'])
def get_all_films():
    try:
        films = Film.query.all()
        if len(films) < 1:
            return jsonify({"msg": "Not found films"}), 404
        serialize_films = list(map( lambda x: x.serialize(), films))
        return serialize_films, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Traer solo una pelicula
@app.route('/films/<int:films_id>', methods=['GET'])
def get_film(films_id):
    try:
        film = Film.query.get(films_id)
        if film is None:
            return jsonify({"msg": f"Not found film: {films_id}"}), 404
        serialized_film = film.serialize()
        return serialized_film, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Crear una pelicula
@app.route('/films', methods=['POST'])
def create_film():
    try:
        body = json.loads(request.data)
        new_film= Film(
            title = body["title"],
            director = body["director"],
            producer = body["producer"],
            release_date = body["release_date"],
            opening_crawl = body["opening_crawl"]
        )
        db.session.add(new_film)
        db.session.commit()
        return jsonify({"msg": "Film: created succefully"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Editar una peli - extra

# Borrar una peli - extra

# Traer todos las especies
@app.route('/species', methods=['GET'])
def get_all_species():
    try:
        species = Species.query.all()
        if len(species) < 1:
            return jsonify({"msg": "Not found species"}), 404
        serialize_species= list(map( lambda x: x.serialize(), species))
        return serialize_species, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Traer solo una especie
@app.route('/species/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    try:
        specie = Species.query.get(specie_id)
        if specie is None:
            return jsonify({"msg": f"Not found film: {specie_id}"}), 404
        serialized_specie= specie.serialize()
        return serialized_specie, 200
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Crear una especie
@app.route('/specie', methods=['POST'])
def create_specie():
    try:
        body = json.loads(request.data)
        new_specie= Species(
            name = body["name"],
            classification = body["classification"],
            designation = body["designation"],
            average_height = body["average_height"],
            average_lifespan = body["average_lifespan"],
            eye_colors = body["eye_colors"],
            hair_colors = body["hair_colors"],
            skin_colors = body["skin_colors"],
            language = body["language"]
        )
        db.session.add(new_specie)
        db.session.commit()
        return jsonify({"msg": "Specie: created succefully"}), 201
    except Exception as e:
        return jsonify({"msg": "Server error", "error": str(e)}), 500

# Editar una especie - extra

# Borrar una especie - extra

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
