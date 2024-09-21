from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    planetas_favoritos = db.relationship('PlanetasFavoritos', backref='usuario')
    personajes_favoritos = db.relationship('PersonajesFavoritos', backref='usuario')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_planeta = db.Column(db.String(250), nullable=False)
    ubicacion_planeta = db.Column(db.String(250), nullable=False)
    habitantes_planeta = db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('PlanetasFavoritos', backref='planeta')

    def serialize(self):
        return {
            "id": self.id,
            "nombre_planeta": self.nombre_planeta,
            "ubicacion_planeta": self.ubicacion_planeta,
            "habitantes": self.habitantes_planeta
        }

class PlanetasFavoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_personaje = db.Column(db.String(250), nullable=False)
    peliculas_personaje = db.Column(db.String(250), nullable=False)
    raza_personaje = db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('PersonajesFavoritos', backref='personaje')

    def serialize(self):
        return {
            "id": self.id,
            "nombre_personaje": self.nombre_personaje,
            "peliculas_personaje": self.peliculas_personaje,
            "raza_personaje": self.raza_personaje
        }

class PersonajesFavoritos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
