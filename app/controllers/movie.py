from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS, DATE_FORMAT
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all movie records
    """
    all_movies = Movie.query.all()
    movies = [{k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS} for movie in all_movies]
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get movie by ID
    """
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error="No ID specified"), 400)

    try:
        movie_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error="ID must be an integer"), 400)

    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return make_response(jsonify(error="Record with such ID does not exist"), 400)

    movie_data = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(movie_data), 200)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    ### YOUR CODE HERE ###
    # Check if required fields exist
    if not data:
        return make_response(jsonify(error="No input data provided"), 400)

    # Validate required fields
    required_fields = ['name', 'genre', 'year']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return make_response(jsonify(error=f"Missing fields: {', '.join(missing_fields)}"), 400)

    # Validate `year`
    try:
        data['year'] = int(data['year'])
    except ValueError:
        return make_response(jsonify(error="Year must be an integer"), 400)

    # Reject invalid fields
    invalid_fields = [field for field in data.keys() if field not in MOVIE_FIELDS]
    if invalid_fields:
        return make_response(jsonify(error=f"Invalid fields: {', '.join(invalid_fields)}"), 400)

    try:
        # Use the create method from models/base.py
        new_movie = Movie.create(**data)
        new_movie_data = {k: v for k, v in new_movie.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(new_movie_data), 200)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 400)
    ### END CODE HERE ###


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    ### YOUR CODE HERE ###
    # Validate 'id'
    if "id" not in data:
        return make_response(jsonify(error="No id specified"), 400)

    try:
        movie_id = int(data["id"])
    except ValueError:
        return make_response(jsonify(error="Id must be an integer"), 400)

    # Check if movie with given ID exists
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return make_response(jsonify(error="Movie with such id does not exist"), 400)

    # Validate input fields
    valid_fields = MOVIE_FIELDS
    invalid_fields = [field for field in data.keys() if field not in valid_fields]
    if invalid_fields:
        return make_response(jsonify(error=f"Invalid fields: {', '.join(invalid_fields)}"), 400)

    # Validate `year` if present
    if "year" in data:
        try:
            data["year"] = int(data["year"])
        except ValueError:
            return make_response(jsonify(error="Year must be an integer"), 400)

    try:
        # Use the update method from models/base.py
        updated_movie = Movie.update(movie_id, **data)
        if not updated_movie:
            return make_response(jsonify(error="Error updating movie record"), 400)

        updated_movie_data = {k: v for k, v in updated_movie.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(updated_movie_data), 200)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 400)
    ### END CODE HERE ###


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()

    ### YOUR CODE HERE ###
    # Validate 'id'
    if "id" not in data:
        return make_response(jsonify(error="No id specified"), 400)

    try:
        movie_id = int(data["id"])
    except ValueError:
        return make_response(jsonify(error="Id must be an integer"), 400)

    # Check if movie with given ID exists
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return make_response(jsonify(error="Movie with such id does not exist"), 400)

    try:
        # Use the delete method from models/base.py
        deleted_movie = Movie.delete(movie_id)
        if not deleted_movie:
            return make_response(jsonify(error="Error deleting movie record"), 400)

        return make_response(jsonify(message="Movie deleted successfully"), 200)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 400)
    ### END CODE HERE ###


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()

    # Validate IDs
    try:
        movie_id = int(data.get('id'))
        actor_id = int(data.get('relation_id'))
    except (ValueError, TypeError):
        return make_response(jsonify(error="ID and relation_id must be integers"), 400)

    try:
        # Query the actor and movie
        actor = Actor.query.filter_by(id=actor_id).first()
        movie = Movie.query.filter_by(id=movie_id).first()

        if actor and movie:
            # Add relation using the provided add_relation method
            movie = Movie.add_relation(movie_id, actor)
            # return make_response(jsonify(message="Relation added successfully"), 200)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        elif not actor:
            return make_response(jsonify(error="Actor not found"), 400)
        elif not movie:
            return make_response(jsonify(error="Movie not found"), 400)
    except Exception as e:
        return make_response(jsonify(error=f"Error occurred: {str(e)}"), 400)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    # Validate IDs
    try:
        movie_id = int(data.get('id'))
    except (ValueError, TypeError):
        return make_response(jsonify(error="ID must be integer"), 400)

    try:
        # Fetch the movie from the database
        movie = Movie.query.filter_by(id=movie_id).first()

        # Check if the movie exists
        if movie:
            # Clear all relations for the movie
            movie = Movie.clear_relations(movie_id)
            # return make_response(jsonify(message="All relations cleared successfully"), 200)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        else:
            return make_response(jsonify(error="Movie not found"), 400)
    except Exception as e:
        # db.session.rollback()
        return make_response(jsonify(error=f"Error occurred: {str(e)}"), 400)
