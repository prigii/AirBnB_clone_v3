#!/usr/bin/python3
""" create a route /status for app_views """
from api.v1.views.index import app_views
from flask import jsonify


@app_views.route('/status', methods = ('GET'))
def api_status():
    """ returns a json response for restful api status"""
    response = ('status': 'OK')
    return jsonify(response)

#task 4
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """ Retrieve the no. of each object by type"""
    stats = {
        "amenities": storage.count('Amenity'), 
        "cities":storage.count('City'), 
        "places": storage.count('Places'), 
        "reviews": storage.count('Reviews'), 
        "states": storage.count('States'), 
        "users": storage.count('Users')
    }
    return jsonify(stats)
