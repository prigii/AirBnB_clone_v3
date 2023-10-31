#!/usr/bin/python3
""" create a new view for review objects and default restful api actions """
from api.v1.views.index import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review


# retrieve all review  objects
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """ retrieve all review objects from a reviews"""
    reviews = storage.all(Review).values()
    # jsonify the list
    review_list = [review.to_dict() for review in reviews]
    return jsonify(review_list)

# retrieve a specific reviews object by ID


@app_views.route('/reviews/<review_id>', method=['GET'], strict_slashes=False)
def get_reviews(reviews_id):
    """ retrieve a reviews object by ID"""
    reviews = storage.get(Review, reviews_id)
    if reviews:
        # return in json format
        return jsonify(reviews.to_dict())
    else:
        # return 404 error in case reviews is not found
        abort(404)
# delete a specific reviews object by ID


@app_views.route('/reviews/<reviews_id>', method=['DELETE'])
def delete_reviews(reviews_id):
    """ delete a reviews object by ID"""
    # get reviews object from storage
    reviews = storage.get(Review, reviews_id)
    if reviews:
        # delete reviews object and save changes
        storage.delete(reviews)
        storage.save()
        # return empty json list with code 200
        return jsonify(()), 200
    else:
        # return 404 error in case reviews is not found
        abort(404)
# create a new reviews object


@app_views.route('/reviews/<reviews_id>', method=['POST'],
                 strict_slashes=False)
def create_reviews(reviews_id):
    """ creates a reviews object """
    if not request.get_json():
        # return 400 error if request not in json format
        abort(400, 'Not a JSON call')
    # get the json data from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # return 400 error if name is missing from json data
        abort(400, 'Name is missing')
    # create a new reviews object with the json data
    reviews = Review(**kwargs)
    # save new object to storage
    reviews.save()
    # return newly created json object
    return jsonify(reviews.to_dict()), 201
# updating existing reviews object by ID


@app_views.route('/reviewss/<reviews_id>', method=['PUT'],
                 strict_slashes=False)
def update_reviews(reviews_id):
    """ updates a reviews object """
    # get the reviews object with given ID
    reviews = storage.get(Review, reviews_id)
    if reviews:
        if not request.get_json():
            # return 400 error if request data not in json format
            abort(400, 'Not a JSON call')
        # get the json data from the request
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        # update the attrib of the object with the json data
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(reviews, key, value)
        # save the updated reviews object to storage
        reviews.save()
        # return updated object in JSON format w/ 200 code
        return jsonify(reviews.to_dict()), 200
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
