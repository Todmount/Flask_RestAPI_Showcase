from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all actor records
    """
    all_actors = Actor.query.all()
    actors = [{k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS} for actor in all_actors]
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get actor by ID
    """
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error="No id specified"), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error="Id must be integer"), 400)

    actor = Actor.query.filter_by(id=row_id).first()
    if not actor:
        return make_response(jsonify(error="Record with such id does not exist"), 400)

    actor_data = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(actor_data), 200)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # Check if required fields exist
    if not data:
        return make_response(jsonify(error="No input data provided"), 400)

    # Check if all required fields specified
    required_fields = ['name', 'gender', 'date_of_birth']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return make_response(jsonify(error=f"Missing fields: {', '.join(missing_fields)}"), 400)

    # Validate `date_of_birth`
    try:
        data["date_of_birth"] = dt.strptime(data["date_of_birth"], DATE_FORMAT).date()
    except ValueError:
        return make_response(jsonify(error=f"Date must be in {DATE_FORMAT} format"), 400)

    try:
        # Use the create method from models/base.py
        new_actor = Actor.create(**data)
        new_actor_data = {k: v for k, v in new_actor.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(new_actor_data), 200)
    except Exception as e:
        # Handle any unexpected errors
        return make_response(jsonify(error=str(e)), 400)

    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    # Validate 'id'
    if "id" not in data:
        return make_response(jsonify(error="No id specified"), 400)
    try:
        actor_id = int(data["id"])
    except ValueError:
        return make_response(jsonify(error="Id must be an integer"), 400)

    # Validate `date_of_birth` if present
    if "date_of_birth" in data:
        try:
            data["date_of_birth"] = dt.strptime(data["date_of_birth"], DATE_FORMAT).date()
        except ValueError:
            return make_response(jsonify(error=f"Date must be in {DATE_FORMAT} format"), 400)
    ######
    # Validate input fields
    invalid_fields = [field for field in data.keys() if field not in ACTOR_FIELDS + ["id"]]
    if invalid_fields:
        return make_response(jsonify(error=f"Invalid fields: {', '.join(invalid_fields)}"), 400)
    ######
    try:
        # Use the update method from models/base.py
        updated_actor = Actor.update(actor_id, **data)
        if not updated_actor:
            return make_response(jsonify(error="Record with such id does not exist"), 400)
        updated_actor_data = {k: v for k, v in updated_actor.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(updated_actor_data), 200)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 400)
    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # Validate ID
    if 'id' not in data:
        return make_response(jsonify(error="No ID specified"), 400)
    try:
        actor_id = int(data['id'])
    except ValueError:
        return make_response(jsonify(error="ID must be an integer"), 400)

    # Find and delete the actor
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        return make_response(jsonify(error="Actor with such ID does not exist"), 400)

    try:
        Actor.delete(actor_id)
        return make_response(jsonify(message="Record successfully deleted"), 200)
    except Exception as e:
        return make_response(jsonify(error=str(e)), 400)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to an actor's filmography.
    """
    data = get_request_data()

    # Validate IDs
    try:
        actor_id = int(data.get('id'))
        movie_id = int(data.get('relation_id'))
    except (ValueError, TypeError):
        return make_response(jsonify(error="ID and relation_id must be integers"), 400)

    try:
        # Query the actor and movie
        actor = Actor.query.filter_by(id=actor_id).first()
        movie = Movie.query.filter_by(id=movie_id).first()

        if actor and movie:
            # Add relation using the provided add_relation method
            actor = Actor.add_relation(actor_id, movie)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        elif not actor:
            return make_response(jsonify(error="Actor not found"), 400)
        elif not movie:
            return make_response(jsonify(error="Movie not found"), 400)
    except Exception as e:
        return make_response(jsonify(error=f"Error occurred: {str(e)}"), 400)


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    # Validate IDs
    try:
        actor_id = int(data.get('id'))
    except (ValueError, TypeError):
        return make_response(jsonify(error="ID must be integer"), 400)

    try:
        # Fetch the actor from the database
        actor = Actor.query.filter_by(id=actor_id).first()

        # Check if the actor exists
        if actor:
            # Clear all relations for the actor
            actor = Actor.clear_relations(actor_id)
            # return make_response(jsonify(message="All relations cleared successfully"), 200)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        else:
            return make_response(jsonify(error="Actor not found"), 400)
    except Exception as e:
        return make_response(jsonify(error=f"Error occurred: {str(e)}"), 400)
