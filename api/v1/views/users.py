#!/usr/bin/python3
""" create a new view for user objects and default restful api actions """
from api.v1.views.index import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User

# retrieve all user objects


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ retrieve all users"""
    users = storage.all(User).values()
    # jsonify the list
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)

# retrieve a specific user object by ID


@app_views.route('/users/<user_id>', method=['GET'], strict_slashes=False)
def get_user(user_id):
    """ retrieve a user object by ID"""
    user = storage.get(User, user_id)
    if user:
        # return in json format
        return jsonify(user.to_dict())
    else:
        # return 404 error in case user is not found
        abort(404)
# delete a specific user object by ID


@app_views.route('/users/<user_id>', method=['DELETE'])
def delete_user(user_id):
    """ delete a user object by ID"""
    # get user object from storage
    user = storage.get(User, user_id)
    if user:
        # delete user object and save changes
        storage.delete(user)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case user is not found
        abort(404)
# create a new user object


@app_views.route('/users/<user_id>', method=['POST'], strict_slashes=False)
def create_user(user_id):
    """ creates a user object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new user object with the json data
    user = User(**kwargs)
    # save new object to storage
    user.save()
    # return newly created json object
    return jsonify(user.to_dict()), 201
# updating existing user object by ID


@app_views.route('/users/<user_id>', method=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a user object """
    # get the user object with given ID
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            # return 400 error if request data not in json format
            abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        # save the updated user object to storage
        user.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(user.to_dict()), 200
    else:
        # return code 404
        abort(404)
# error handler


@app_views.errorhandler(404)
def not_found(error):
    """ raise code 404 """
    # return a json response for 404 error
    response = [{'error': 'Not found'}]
    return jsonify(response), 404


@app_views.errorhandler(400)
def bad_request(error):
    """ raise 400 code for bad request"""
    # return json response for 400 error
    response = [{'error': 'Bad request'}]
    return jsonify(response), 400
