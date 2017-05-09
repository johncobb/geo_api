from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload

from app.mod_geo.models.landmark import Landmark
from app.mod_geo.models.geometry import Geometry
from app import ApiExceptionHandler as ApiException
from sqlalchemy import exc

bp_landmark = Blueprint('landmark', __name__, url_prefix='/landmark')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_landmark.route('/<int:landmarkId>', methods=['GET'])
def get_landmark_byid(landmarkId):

    """
    Query Landmark.

    Parameters
    ----------
    landmarkId : int
        Landmark Identifier

    Returns
    -------
    JSON
        Landmark in JSON format
    """

    try:
        landmark = Landmark.query.filter_by(id=landmarkId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if landmark is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":landmark.to_json()})

@bp_landmark.route('/', methods=['GET'])
def get_landmarks():

    """
    Query Landmarks.

    Returns
    -------
    JSON dict
        Landmarks in JSON dict format
    """

    try:
        landmarks = Landmark.query.filter_by(archive=False).all()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(landmarks) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [s.to_json() for s in landmarks]})

@bp_landmark.route('/', methods=['POST'])
def add_landmark():

    """
    Add Landmark.

    Parameters
    ----------
    POST : JSON
        JSON object (Landmark)

    Returns
    -------
    JSON
        Landmark in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = request.get_json()

        x = data['geometry']['coordinates'][0]
        y = data['geometry']['coordinates'][1]
        #sql_polygon = 'POLYGON ((%s %s))'
        sql_polygon = 'POINT (%s %s)'
        sql_polygon = sql_poljjon % (x, y)

        print sql_polygon
        groupId = data['properties']['groupId']
        path = data['properties']['path']

    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    # Create the object
    landmark = Landmark(groupId, path, sql_polygon)

    try:
        db.session.add(landmark)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    #return jsonify({"data":landmark.to_json()})
    return jsonify(data)

@bp_landmark.route('/<int:landmarkId>', methods=['PUT'])
def update_landmark(landmarkId):

    """
    Update Landmark.

    Parameters
    ----------
    landmarkId : int
        Landmark Identifier

    Returns
    -------
    JSON
        Landmark in JSON format
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
        landmark = Landmark.query.filter_by(id=landmarkId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    # Find the reord to update

    if landmark is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    landmark.groupId = p.groupId
    landmark.alias = p.alias
    landmark.ip = p.ip
    landmark.model = p.model
    landmark.serial = p.serial
    landmark.fw = p.fw

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":landmark.to_json()})

@bp_landmark.route('/<int:landmarkId>', methods=['DELETE'])
def delete_landmark(landmarkId):

    """
    Delete Landmark.

    Parameters
    ----------
    landmarkId : int
        Landmark Identifier

    Returns
    -------
    JSON
        Landmark in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true
    try:
        landmark = Landmark.query.filter_by(id=landmarkId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)


    if landmark is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    # Update the object
    landmark.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":landmark.to_json()})

