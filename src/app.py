import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, PlanetasFavoritos, PersonajesFavoritos, Planetas, Personajes

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
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

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints para crear, obtener y gestionar usuarios
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'msg': 'campos requeridos'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'El usuario ya existe'}), 400
    
    new_user = User(email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'Usuario creado con éxito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]  
    return jsonify(serialized_users), 200 

@app.route('/usuarios/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize()), 200  
    else:
        return jsonify({"msg": "Usuario no encontrado"}), 404

# Endpoints para obtener personajes y planetas
@app.route('/people', methods=['GET'])
def get_all_personajes():
    personajes = Personajes.query.all()
    serialized_personajes = [personaje.serialize() for personaje in personajes] 
    return jsonify(serialized_personajes), 200

@app.route('/people/<int:personaje_id>', methods=['GET'])
def get_personaje_by_id(personaje_id):
    personaje = Personajes.query.get(personaje_id)
    if personaje:
        return jsonify(personaje.serialize()), 200  
    else:
        return jsonify({"msg": "Personaje no encontrado"}), 404

@app.route('/planets', methods=['GET'])
def get_all_planetas():
    planetas = Planetas.query.all()
    serialized_planetas = [planeta.serialize() for planeta in planetas]
    return jsonify(serialized_planetas), 200

@app.route('/planets/<int:planeta_id>', methods=['GET'])
def get_planeta_by_id(planeta_id):
    planeta = Planetas.query.get(planeta_id)
    if planeta:
        return jsonify(planeta.serialize()), 200 
    else:
        return jsonify({"msg": "Planeta no encontrado"}), 404

# Endpoints para agregar planetas y personajes
@app.route('/planets', methods=['POST'])
def agregar_planeta():
    data = request.get_json()
    nombre_planeta = data.get('nombre_planeta')
    ubicacion_planeta = data.get('ubicacion_planeta')
    habitantes_planeta = data.get('habitantes_planeta')

    if not nombre_planeta or not ubicacion_planeta or not habitantes_planeta:
        return jsonify({'msg': 'Error campos obligatorios'}), 400
    
    if Planetas.query.filter_by(nombre_planeta=nombre_planeta).first():
        return jsonify({'msg': 'El planeta ya existe'}), 400
    
    nuevo_planeta = Planetas(nombre_planeta=nombre_planeta, ubicacion_planeta=ubicacion_planeta, habitantes_planeta=habitantes_planeta)

    try:
        db.session.add(nuevo_planeta)
        db.session.commit()
        return jsonify({'msg': 'Planeta agregado con éxito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

@app.route('/people', methods=['POST'])
def agregar_personaje():
    data = request.get_json()
    nombre_personaje = data.get('nombre_personaje')
    peliculas_personaje = data.get('peliculas_personaje')
    raza_personaje = data.get('raza_personaje')

    if not nombre_personaje or not peliculas_personaje or not raza_personaje:
        return jsonify({'msg': 'Error campos obligatorios'}), 400
    
    if Personajes.query.filter_by(nombre_personaje=nombre_personaje).first():
        return jsonify({'msg': 'El personaje ya existe'}), 400
    
    nuevo_personaje = Personajes(nombre_personaje=nombre_personaje, peliculas_personaje=peliculas_personaje, raza_personaje=raza_personaje)

    try:
        db.session.add(nuevo_personaje)
        db.session.commit()
        return jsonify({'msg': 'Personaje agregado con éxito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500

# Endpoints para gestionar favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    planet = Planetas.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msg": "Usuario o planeta no encontrado"}), 404

    existing_fav = PlanetasFavoritos.query.filter_by(user_id=user_id, planeta_id=planet_id).first()
    if existing_fav:
        return jsonify({"msg": "El planeta ya está en la lista de favoritos"}), 400

    new_favorite = PlanetasFavoritos(user_id=user_id, planeta_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people_favorite(people_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    people = Personajes.query.get(people_id)

    if not user or not people:
        return jsonify({"msg": "Usuario o personaje no encontrado"}), 404

    existing_fav = PersonajesFavoritos.query.filter_by(user_id=user_id, personaje_id=people_id).first()
    if existing_fav:
        return jsonify({"msg": "El personaje ya está en la lista de favoritos"}), 400

    new_favorite = PersonajesFavoritos(user_id=user_id, personaje_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje añadido a favoritos"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorite = PlanetasFavoritos.query.filter_by(user_id=user_id, planeta_id=planet_id).first()

    if not favorite:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite(people_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    favorite = PersonajesFavoritos.query.filter_by(user_id=user_id, personaje_id=people_id).first()

    if not favorite:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
