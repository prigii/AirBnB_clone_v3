#!/usr/bin/python3
""" create a new view for amenity objects and default restful api actions """
from api.v1.views.index import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity

# retrieve all amenity objects
@app_views.route('/amenities?', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ retrieve all amenities"""
    amenitiess = storage.all(Amenity).values()
    # jsonify the list
    amenities_list = [amenities.to_dict() for amenities in amenitiess]
    return jsonify(amenities_list)

# retrieve a specific amenities object by ID
@app_views.route('/amenities/<amenity_id>', method=['GET'], strict_slashes=False)
def get_amenities(amenities_id):
    """ retrieve a amenities object by ID"""
    amenities = storage.get(Amenity, amenities_id)
    if amenities:
        # return in json format
        return jsonify(amenities.to_dict())
    else:
        # return 404 error in case amenities is not found
        abort(404)
# delete a specific amenities object by ID
@app_views.route('/amenitiess/<amenities_id>', method=['DELETE'])
def delete_amenities(amenities_id):
    """ delete a amenities object by ID"""
    # get amenities object from storage
    amenities = storage.get(Amenity, amenities_id)
    if amenities:
        # delete amenities object and save changes
        storage.delete(amenities)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case amenities is not found
        abort(404)
# create a new amenities object 
@app_views.route('/amenitiess/<amenities_id>', method=['POST'], strict_slashes=False)
def create_amenities(amenities_id):
    """ creates a amenities object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new amenities object with the json data
    amenities = Amenity(**kwargs)
    # save new object to storage
    amenities.save()
    # return newly created json object
    return jsonify(amenities.to_dict()), 201
# updating existing amenities object by ID
@app_views.route('/amenitiess/<amenities_id>', method=['PUT'], strict_slashes=False)
def update_amenities(amenities_id):
    """ updates a amenities object """
    # get the amenities object with given ID
    amenities = storage.get(Amenity, amenities_id)
    if amenities:
        if not request.get_json():
        # return 400 error if request data not in json format
            abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr (amenities, key, value)
        # save the updated amenities object to storage
        amenities.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(amenities.to_dict()), 200
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
