from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Planet, Character, Favorite

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# [POST] /post-new-user - Crear un nuevo usuario
@app.route('/post-new-user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        email=data.get('email'),
        password=data.get('password'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


# [POST] /post-new-planet - Crear un nuevo planeta
@app.route('/post-new-planet', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet = Planet(
        name=data.get('name'),
        climate=data.get('climate'),
        terrain=data.get('terrain')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201


# [POST] /post-new-character - Crear un nuevo personaje
@app.route('/post-new-character', methods=['POST'])
def create_character():
    data = request.get_json()
    new_character = Character(
        name=data.get('name'),
        height=data.get('height'),
        weight=data.get('weight'),
        gender=data.get('gender')
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201


# [GET] /get-all-characters - Listar todos los registros de personajes (characters)
@app.route('/get-all-characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


# [GET] /get-character-by-id/<int:character_id> - Muestra la información de un solo personaje según su id
@app.route('/get-character-by-id/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if character:
        return jsonify(character.serialize()), 200
    return jsonify({"error": "Character not found"}), 404


# [GET] /get-all-planets - Listar todos los registros de planetas
@app.route('/get-all-planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


# [GET] /get-planet-by-id/<int:planet_id> - Muestra la información de un solo planeta según su id
@app.route('/get-planet-by-id/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"error": "Planet not found"}), 404


# [GET] /get-all-users - Listar todos los usuarios
@app.route('/get-all-users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


# [GET] /get-user-favorites/<int:user_id> - Listar todos los favoritos del usuario especificado
@app.route('/get-user-favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify([favorite.serialize() for favorite in user.favorites]), 200
    return jsonify({"error": "User not found"}), 404


# [POST] /add-favorite-planet/<int:user_id>/<int:planet_id> - Añade un nuevo planeta favorito para un usuario específico
@app.route('/add-favorite-planet/<int:user_id>/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'error': 'Planet not found'}), 404

    new_favorite = Favorite(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': f'Planet {planet.name} added to favorites for user {user.first_name}'}), 200

# [POST] /add-favorite-character/<int:user_id>/<int:character_id> - Añade un nuevo personaje favorito para un usuario específico
@app.route('/add-favorite-character/<int:user_id>/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    character = Character.query.get(character_id)
    if not character:
        return jsonify({'error': 'Character not found'}), 404

    new_favorite = Favorite(user_id=user.id, character_id=character.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({'message': f'Character {character.name} added to favorites for user {user.first_name}'}), 200


# [DELETE] /delete-favorite-character/<int:user_id>/<int:character_id> - Elimina un personaje favorito de un usuario específico
@app.route('/delete-favorite-character/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favorite = Favorite.query.filter_by(user_id=user.id, character_id=character_id).first()
    if not favorite:
        return jsonify({'error': 'Favorite character not found'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite character deleted'}), 200


# [DELETE] /delete-favorite-planet/<int:user_id>/<int:planet_id> - Elimina un planeta favorito de un usuario específico
@app.route('/delete-favorite-planet/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({'error': 'Favorite planet not found'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet deleted'}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
