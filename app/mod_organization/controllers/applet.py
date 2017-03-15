from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload


from app.mod_organization.models.applet import Applet

bp_applet = Blueprint('applet', __name__, url_prefix='/applet')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_applet.route('/<int:appletId>', methods=['GET'])
def get_applet(appletId):
    """
    Query Applet.

    Parameters
    ----------
    appletId : int
        Applet Identifier

    Returns
    -------
    JSON
        Applet in JSON format
    """

    try:
        app = Applet.query.filter_by(id=appletId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if app is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":app.to_json()})

@bp_applet.route('/<int:appId>', methods=['GET'])
def get_applets(appId):
    """
    Query Applets.

    Returns
    -------
    JSON dict
        Applets in JSON dict format
    """

    apps = Applet.query.filter_by(appId=appId).filter_by(archive=False).all()

    if len(apps) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [a.to_json() for a in apps]})

@bp_applet.route('/', methods=['POST'])
def add_applet():
    """
    Add Applet.

    Parameters
    ----------
    POST : JSON
        JSON object (Applet)

    Returns
    -------
    JSON
        Applet in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
    # Create the object
    a = Applet(p.appId, p.name)

    try:
        db.session.add(a)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":a.to_json()})

@bp_applet.route('/<int:appletId>', methods=['PUT'])
def update_applet(appletId):
    """
    Update Applet.

    Parameters
    ----------
    appletId : int
        Applet Identifier

    Returns
    -------
    JSON
        Applet in JSON format
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
        a = Applet.query.filter_by(id=appletId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if a is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT


    # Update the object
    a.name = p.name

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":a.to_json()})

@bp_applet.route('/<int:appletId>', methods=['DELETE'])
def delete_applet(appletId):
    """
    Delete Applet.

    Parameters
    ----------
    appletId : int
        Applet Identifier

    Returns
    -------
    JSON
        Applet in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true

    try:
        a = Applet.query.filter_by(id=appletId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if a is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

   # Prevent orphaning of records 
    assigned = ScannerApplet.query.filter_by(appletId=appletId)\
                            .filter_by(archive=False)\
                            .count()
    if assigned > 0:
        raise ApiException("Cannot delete non-empty applet.", status_code=status.HTTP_409_CONFLICT)
    # End Prevent orphaning of records

    # Update the object
    a.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":a.to_json()})
