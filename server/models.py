from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Movie(db.Model, SerializerMixin):
    __tablename__='movie_table'

    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.String)
    title = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Integer, Nullable = False)
    description = db.Column(db.String)

credit_movie_relationship = db.relationship('Credit', back_populates= 'movie_relationship')


@validates('rating')
def validates_rating(self, key, rating):
    if  1 <= rating >= 10:
        return rating
    else:
        raise ValueError("Not a Valid Rating, must be between 1 and 10.")

@validates('genre')
def validates_genre(self, key, genre): 
    valid_genre = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Thriller', 'Science Fiction', 'Fantasy', 'Mystery', 'Adventure', 'Crime', 'Family', 'Animation', 'Documentary', 'War']
    if genre in valid_genre:
        return valid_genre
    else:
        raise ValueError("Not a valid genre.")

class Credit(db.Model, SerializerMixin):
    __tablename__='credit_table'

    id = db.Column(db.Integer, primary_key = True)
    actor_id = db.Column(db.Integer, Nullable = False)
    movie_id = db.Column(db.Integer, Nullable = False)
    role = db.Column(db.String, Nullable = False)

    actor_id = db.Column(db.Integer, db.ForeignKey('actor_table.id'))
    actor_relationship = db.relationship('Axtor', back_populates='credit_actor_relationship')


    movie_id = db.Column(db.Integer, db.ForeignKey('movie_table.id'))
    movie_relationship = db.relationship('Movie', back_populates='credit_movie_relationship')

    @validates('roles')
    def validates_roles(self, key, roles): 
        valid_roles = ['Performer', 'Director', 'Producer', 'Playwright', 'Lighting Design', 'Sound Design', 'Set Dersign']
        if roles in valid_roles:
            return valid_roles
        else:
            raise ValueError("Not a valid role.")


class Actor(db.Model, SerializerMixin):
    __tablename__='actor_table'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, Nullable = False)
    age = db.Column(db.String, Nullable = False)

    credit_actor_relationship = db.relationship('Credit', back_populates = 'actor_relationship')

    @validates('age')
    def validate_age(self, key, age):
        if not age >= 10:
            raise ValueError("Invalid age, must be at least 10 years old.")
        return age




       
    
