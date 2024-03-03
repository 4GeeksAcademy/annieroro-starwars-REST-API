from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(16), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'

    def serialize(self):
        return {"id": self.id,
                "email": self.email,
                'is_active': self.is_active}


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Planet: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<Character: {self.id} - {self.name}>'

    def serialize(self):
        return {"id": self.id,
                "name": self.name}


# He quitado algunas clases para hacer más fácil el código y no liarme tanto.
"""class Films(db.Model):
    __tablename__ = 'films'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(150), nullable=False)
    director = db.Column(String(150), nullable=False)
    year = db.Column(DateTime)"""


"""class CharactersFilms(db.Model):
    __tablename__ = 'characters_films'
    id = db.Column(Integer, primary_key=True)
    minutes = db.Column(DateTime)
    character_id = db.Column(Integer, ForeignKey('character.id'))
    film_id = db.Column(Integer, ForeignKey('films.id'))
    character = db.relationship('Characters', foreign_keys=['character_id'])
    films = db.relationship('Films', foreign_keys=['film_id'])"""


class FavoritePlanets(db.Model):
    __tablename__  = 'favorite_planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', foreign_keys=[planet_id])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Favorites: {self.id} - User: {self.user_id} - Planet: {self.planet_id}>'

    def serialize(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "name": self.planets.name,
                'planet_id': self.planet_id}


class FavoriteCharacters(db.Model):
    __tablename__ = 'favorite_characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('Users', foreign_keys=[user_id])
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship('Characters', foreign_keys=[character_id])

    def __repr__(self):
        return f'<Favorites: {self.id} - User:{self.user_id} - Character: {self.character_id}>' 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.character.name,
            'character_id': self.character_id
            # do not serialize the password, its a security breach
        }