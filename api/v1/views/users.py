#!/usr/bin/python3
""" create a new view for city objects and default restful api actions """
from api.v1.views.index import app_views
from flask import jsonify, request
from models import storage
from models.user import User

# retrieve all user objects
@app_views.route('/users', methods=['GET'], strict_slashes=FALSE)
def get_all_users():
    """ retrieve all users"""
    states = storage.all(User).values()
    # jsonify the list
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)

# retrieve a specific state object by ID
@app_views.route('/states/<state_id>', method=['GET'], strict_slashes=FALSE)
def get_state(state_id):
    """ retrieve a state object by ID"""
    state = storage.get(State, state_id)
    if state:
        # return in json format
        return jsonify(state.to_dict())
    else:
        # return 404 error in case state is not found
        abort(404)
# delete a specific state object by ID
@app_views.route('/states/<state_id>', method=['DELETE'])
def delete_state(state_id):
    """ delete a state object by ID"""
    # get state object from storage
    state = storage.get(State, state_id)
    if state:
        # delete state object and save changes
        storage.delete(state)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case state is not found
        abort(404)
# create a new state object 
@app_views.route('/states/<state_id>', method=['POST'], strict_slashes=FALSE)
def create_state(state_id):
    """ creates a state object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new state object with the json data
    state = State(**kwargs)
    # save new object to storage
    state.save()
    # return newly created json object
    return jsonify(state.to_dict()), 201
# updating existing state object by ID
@app_views.route('/states/<state_id>', method=['PUT'], strict_slashes=FALSE)
def update_state(state_id):
    """ updates a state object """
    # get the state object with given ID
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
        # return 400 error if request data not in json format
        abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr (state, key, value)
        # save the updated state object to storage
        state.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(state.to_dict()), 200
    else:
        # return code 404
        abort(404) 
# error handler
@app_views.errorhandler(404)
def not_found(error):
    """ raise code 404 """
    # return a json response for 404 error
    response = ['error': 'Not found']
    return jsonify(response), 404

@app_views.errorhandler(400)
def bad_request(error):
    """ raise 400 code for bad request"""
    # return json response for 400 error
    response = ['error': 'Bad request']
    return jsonify(response), 400
