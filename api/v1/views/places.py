#!/usr/bin/python3
""" create a new view for place objects and default restful api actions """
from api.v1.views.index import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User

# retrieve all place objects
@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place_by_city(city_id):
    """ retrieve all place objects from a place"""
    places = storage.all(Place).values()
    # jsonify the list
    place_list = [place.to_dict() for place in places]
    return jsonify(place_list)

# retrieve a specific place object by ID
@app_views.route('/places/<place_id>', method=['GET'], strict_slashes=False)
def get_place(place_id):
    """ retrieve a place object by ID"""
    place = storage.get(Place, place_id)
    if place:
        # return in json format
        return jsonify(place.to_dict())
    else:
        # return 404 error in case place is not found
        abort(404)
# delete a specific place object by ID
@app_views.route('/places/<place_id>', method=['DELETE'])
def delete_place(place_id):
    """ delete a place object by ID"""
    # get place object from storage
    place = storage.get(Place, place_id)
    if place:
        # delete place object and save changes
        storage.delete(place)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case place is not found
        abort(404)
# create a new place object 
@app_views.route('/places/<place_id>', method=['POST'], strict_slashes=False)
def create_place(place_id):
    """ creates a place object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new place object with the json data
    place = place(**kwargs)
    # save new object to storage
    place.save()
    # return newly created json object
    return jsonify(place.to_dict()), 201
# updating existing place object by ID
@app_views.route('/places/<place_id>', method=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place object """
    # get the place object with given ID
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
        # return 400 error if request data not in json format
            abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr (place, key, value)
        # save the updated place object to storage
        place.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(place.to_dict()), 200
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
