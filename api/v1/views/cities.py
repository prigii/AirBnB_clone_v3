#!/usr/bin/python3
""" create a new view for city objects and default restful api actions """
from api.v1.views.index import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
from models.city import City

# retrieve all city objects


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_by_states(state_id):
    """ retrieve all city objects from a cities"""
    cities = storage.all(City).values()
    # jsonify the list
    cities_list = [cities.to_dict() for city in cities]
    return jsonify(cities_list)

# retrieve a specific cities object by ID


@app_views.route('/cities/<city_id>', method=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieve a city object by ID"""
    city = storage.get(City, city_id)
    if city:
        # return in json format
        return jsonify(city.to_dict())
    else:
        # return 404 error in case cities is not found
        abort(404)
# delete a specific cities object by ID


@app_views.route('/cities/<city_id>', method=['DELETE'])
def delete_city(city_id):
    """ delete a cities object by ID"""
    # get city object from storage
    city = storage.get(City, city_id)
    if city:
        # delete city object and save changes
        storage.delete(city)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case cities is not found
        abort(404)
# create a new city object


@app_views.route('/cities/<city_id>', method=['POST'], strict_slashes=False)
def create_city(city_id):
    """ creates a city object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new cities object with the json data
    city = city(**kwargs)
    # save new object to storage
    city.save()
    # return newly created json object
    return jsonify(city.to_dict()), 201
# updating existing city object by ID


@app_views.route('/cities/<city_id>', method=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updates a city object """
    # get the cities object with given ID
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            # return 400 error if request data not in json format
            abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        # save the updated cities object to storage
        city.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(city.to_dict()), 200
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
