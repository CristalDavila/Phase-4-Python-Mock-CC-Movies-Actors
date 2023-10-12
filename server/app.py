#!/usr/bin/env python3

from models import db, Movie, Actor, Credit
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os
from flask import func 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return ''


#GET /actors

@app.get('/actors')
def get_actors():
    actors = Actor.query.all():
    data = [actor.to_dict(only=('name', 'age')) for actor in actors]

    return make_response(
        jsonify(data),
        200
    )
#GET /actors/int:id

@app.get('/actors/<int:id>')
def get_actor_by_id(id):
    actor = Actor.query.filter(Actor.id == id).first()

    if not actor: 
        return make_response(
            jsonify({"error": "actor not found"})
            404
        )
#POST /actors

@app.post('/actors')
def post_actor():
    data = request.get_json()

    try:
        new_actor = Actor(
            name=data.get("name")
            age=data.get("age")
        )
        db.session.add(new_actor)
        db.session.commit()

        return make_response(
            jsonify(new_actor.to_dict(only=('name', 'age', 'id'))),
            201
        )
    except ValueError:
        return make_response(
            jsonify({"error": ["validation errors"]})
            406
        )

#PATCH /actors/:id

@app.patch('/actors/<int:id>')
def patch_actor_by_id(id):
    actor = Actor.query.filter(Actor.id == id).first()
    data = request.get_json()

    if not actor:
        return make_response(
            jsonify({"error": "actor not found."}),
            404
        )
    try: 
        for field in data:
            setattr(actor, field, data[field])
            db.session.add(actor)
            db.session.commit()

        return make_response(
            jsonify(actor.to_dict(only=('name', 'age', 'id')))
            202
        )
    except ValueError as e:
        print(e.__str__())
        return make_response(
            jsonify({"error": ["validation errors."]})
            406
        )

#DELETE /actors/int:id

@app.delete('/actors/<int:id>')
def delete_actor(id):
    actor = Actor.query.filter(Actor.id == id).first()

    if not actor: 
        return make_response(
            jsonify({"error": "Actor Not Found"}),
            404
        )
    db.sesssion.delete(actor)
    db.session.commit()

    return make_response(jsonify({}), 204
)

#GET /movies

@app.get('/movies')
def get_movies():
    movies = Movie.query.all()
    data = [movie.to_dict(only=('image', 'title', 'genre', 'rating', 'description')) for movie in movies]

    return make_response(
        jsonify(data),
        200
    )


#POST /movies

@app.post('/movies')
def post_movie():
    data = request.get_json()

    try:
        new_movie = Movie(
            image=data.get("image")
            title=data.get("title")
            genre=data.get("genre")
            rating=data.get("rating")
            description=data.get("description")

        )
        db.session.add(new_movie)
        db.session.commit()

        return make_response(
            jsonify(new_movie.to_dict(only="title")),
            201
        )
    except ValueError:
        return make_response(
            jsonify({"error": ["validation errors"]}),
            406
        )


if __name__ == '__main__':
    app.run(port=5555, debug=True)