"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, FavoritePlanets, FavoriteCharacters, Characters, Planets
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

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    response_body = {}
    if request.method == 'GET':
        users = db.session.execute(db.select(Users)).scalars()
        response_body['results'] = [row.serialize() for row in users]
        response_body['message'] = 'Data retrieved successfully!'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        user = Users(email = data['email'],
                     password = data['password'],
                     is_active = True)
        db.session.add(user)
        db.session.commit()
        response_body['results'] = user.serialize()
        response_body['message'] = 'Metodo POST de users'
        return response_body, 200


@app.route('/users/<int:user_id>', methods=['GET'])
def handle_user(user_id):
    response_body = {}
    results = []
    users = db.session.execute(db.select(Users).where(Users.id == user_id)).scalar()
    response_body['results'] = users.serialize()
    response_body['message'] = f'Recibiendo user {user_id}'
    return response_body, 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def handle_favorites(user_id):
    response_body = {}
    results = {}
    favorite_planets = db.session.execute(db.select(FavoritePlanets)).scalars()
    favorite_characters = db.session.execute(db.select(FavoriteCharacters)).scalars()
    results['favorite_planets'] = [row.serialize() for row in favorite_planets]
    results['favorite_characters'] = [row.serialize() for row in favorite_characters]
    response_body['results'] = results
    response_body['message'] = 'Data retrieved successfully!'
    return response_body, 200


@app.route('/characters', methods=['GET'])
def handle_characters():
    response_body = {}
    results = []
    character = db.session.execute(db.select(Characters)).scalars()
    response_body['results'] = [row.serialize() for row in character]
    response_body['message'] = 'Metodo GET characters OK!'
    return response_body, 200


@app.route('/characters/<int:id_character>', methods=['GET'])
def handle_character_id(id_character):
        response_body = {}
        results = {}
        character = db.session.execute(db.select(Characters).where(Characters.id == id_character)).scalar()
        response_body['results'] = character.serialize()
        response_body['message'] = 'Successful!'

        return response_body, 200


@app.route('/favorites/<int:user_id>/characters', methods=['POST'])
def add_favorite_characters(user_id):
    response_body = {}
    data = request.json
    favorite = FavoriteCharacters(user_id = user_id,
                                  character_id = data['character_id'])
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = f'Responde el POST {user_id}'
    
    return response_body


@app.route('/planets', methods=['GET'])
def handle_planets():
    response_body = {}
    results = []
    planet = db.session.execute(db.select(Planets)).scalars()
    response_body['results'] = [row.serialize() for row in planet]
    response_body['message'] = 'Metodo GET planets OK!'
    return response_body, 200


@app.route('/planets/<int:id_planet>', methods=['GET'])
def handle_planet_id(id_planet):
    response_body = {}
    results = []
    planet = db.session.execute(db.select(Planets).where(Planets.id == id_planet)).scalar()
    response_body['results'] = planet.serialize()
    response_body['message'] = 'Successful!'
    return response_body, 200


@app.route('/favorites/<int:user_id>/planets', methods=['POST'])
def add_favorite_planets(user_id):
    response_body = {}
    data = request.json
    favorite = FavoritePlanets(user_id = user_id,
                               planet_id = data['planet_id'])
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = f'Responde el POST {user_id}'
    
    return response_body


@app.route('/favorites/<int:user_id>/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planets(user_id, planet_id):
    response_body = {}
    planet = db.session.execute(db.select(FavoritePlanets).where(FavoritePlanets.user_id == user_id)).scalar()
    db.session.delete(planet)
    db.session.commit()
    response_body['message'] = f'Planet {planet_id} deleted to favorites of {user_id}'
    return response_body, 200


@app.route('/favorites/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    response_body = {}
    character = db.session.execute(db.select(FavoriteCharacters).where(FavoriteCharacters.user_id == user_id)).scalar()
    db.session.delete(character)
    db.session.commit()
    response_body['message'] = f'Character {character_id} deleted to favorites of {user_id}'
    return response_body, 200

    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
