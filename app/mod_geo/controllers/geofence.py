from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload

from app.mod_geo.models.geofence import GeoFence
from app import ApiExceptionHandler as ApiException
from sqlalchemy import exc

bp_geofence = Blueprint('geofence', __name__, url_prefix='/geofence')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_geofence.route('/<int:geoFenceId>', methods=['GET'])
def get_geofence_byid(geoFenceId):

    """
    Query GeoFence.

    Parameters
    ----------
    geoFenceId : int
        GeoFence Identifier

    Returns
    -------
    JSON
        GeoFence in JSON format
    """

    try:
        geofence = GeoFence.query.filter_by(id=geoFenceId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if geofence is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":geofence.to_json()})

@bp_geofence.route('/', methods=['GET'])
def get_geofences():

    """
    Query GeoFences.

    Returns
    -------
    JSON dict
        GeoFences in JSON dict format
    """

    try:
        geofences = GeoFence.query.filter_by(archive=False).all()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(geofences) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [s.to_json() for s in geofences]})

@bp_geofence.route('/', methods=['POST'])
def add_geofence():

    """
    Add GeoFence.

    Parameters
    ----------
    POST : JSON
        JSON object (GeoFence)

    Returns
    -------
    JSON
        GeoFence in JSON format
    """

    data = None
    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    # Create the object
    geofence = GeoFence(p.groupId, p.alias, p.points)

    try:
        db.session.add(geofence)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":geofence.to_json()})

@bp_geofence.route('/<int:geoFenceId>', methods=['PUT'])
def update_geofence(geoFenceId):

    """
    Update GeoFence.

    Parameters
    ----------
    geoFenceId : int
        GeoFence Identifier

    Returns
    -------
    JSON
        GeoFence in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
   # Find the record to update 
    try:
        geofence = GeoFence.query.filter_by(id=geoFenceId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    # Find the reord to update

    if geofence is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    geofence.groupId = p.groupId
    geofence.alias = p.alias
    geofence.points = p.points

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":geofence.to_json()})

@bp_geofence.route('/<int:geoFenceId>', methods=['DELETE'])
def delete_geofence(geoFenceId):

    """
    Delete GeoFence.

    Parameters
    ----------
    geoFenceId : int
        GeoFence Identifier

    Returns
    -------
    JSON
        GeoFence in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true
    try:
        geofence = GeoFence.query.filter_by(id=geoFenceId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)


    if geofence is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    # Update the object
    geofence.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":geofence.to_json()})

