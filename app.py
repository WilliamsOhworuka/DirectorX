from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth.auth import requires_auth, AuthError

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES

    @app.route('/')
    def home_page():
        return jsonify({
            'message': 'Welcome to Casting Agency'
        }), 200

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors_data = Actor.query.all()
        actors = [actor.format() for actor in actors_data]

        return jsonify({
            "success": True,
            "actors": actors
        })

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies_data = Actor.query.all()
        movies = [movie.format() for movie in movies_data]

        return jsonify({
            "success": True,
            "movies": movies
        })


    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_actors(payload):
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            if not name or not age or not gender: 
                raise AuthError({}, 400)

            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                "success": True,
                "actor": actor.format() 
            })
        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movies(payload):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('releaseDate', None)

        try:
            if not title or not release_date: 
                raise AuthError({},400)

            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                "success": True,
                "movie": movie.format() 
            })
        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actor(payload, id):
        body = request.get_json()

        try:
            actor = Actor.query.get(id)

            if actor is None:
                raise AuthError({},404)

            name = body.get('name', None)
            
            if name is None or type(name) is not str or len(name) == 0:
                raise AuthError({},400)
            
            actor.name = name
            age = body.get('age', None)

            if age is None or type(int(age)) is not int:
                raise AuthError({},400)

            actor.age = age
            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format(),
            })

        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movies(payload, id):
        body = request.get_json()

        try:
            movie = Movie.query.get(id)

            if movie is None:
                raise AuthError({},404)

            title = body.get('title', None)

            if not title or type(title) is not str or len(title) == 0:
                raise AuthError({},400)

            movie.title = title
            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format(),
            })

        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(422)


    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def remove_actors(payload, id):
        actor = Actor.query.get(id)

        try:
            if not actor:   
                raise AuthError({} , 404)
        
            actor.delete()

            return jsonify({
                "success": True,
                "delete": id
            })

        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(500)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def remove_movies(payload, id):
        movie = Movie.query.get(id)

        try:
            if not movie:
                raise AuthError({},404)

            movie.delete()

            return jsonify({
                "success": True,
                "delete": id
            })

        except AuthError as error:
            (err,code) = error.args
            abort(code)
        except Exception:
            abort(500)


    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400


    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized",
        }), 401


    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden",
        }), 403

    return app
    
app = create_app()

if __name__ == '__main__':
    app.run()