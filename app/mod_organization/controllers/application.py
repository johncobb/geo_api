from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload


from app.mod_organization.models.application import App

bp_app = Blueprint('app', __name__, url_prefix='/app')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_app.route('/<int:appId>', methods=['GET'])
def get_app(appId):
    """
    Query App.

    Parameters
    ----------
    appId : int
        App Identifier

    Returns
    -------
    JSON
        App in JSON format
    """

    try:
        app = App.query.filter_by(id=appId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if app is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":app.to_json()})

@bp_app.route('/', methods=['GET'])
def get_apps():
    """
    Query Apps.

    Returns
    -------
    JSON dict
        Apps in JSON dict format
    """

    apps = App.query.filter_by(archive=False)

    if apps is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [a.to_json() for a in apps]})

@bp_app.route('/', methods=['POST'])
def add_app():
    """
    Add App.

    Parameters
    ----------
    POST : JSON
        JSON object (App)

    Returns
    -------
    JSON
        App in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
    # Create the object
    a = App(p.name)

    try:
        db.session.add(a)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":a.to_json()})

@bp_app.route('/<int:appId>', methods=['PUT'])
def update_app(appId):
    """
    Update App.

    Parameters
    ----------
    appId : int
        App Identifier

    Returns
    -------
    JSON
        App in JSON format
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
        a = App.query.filter_by(id=appId).first()
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

@bp_app.route('/<int:appId>', methods=['DELETE'])
def delete_app(appId):
    """
    Delete App.

    Parameters
    ----------
    appId : int
        App Identifier

    Returns
    -------
    JSON
        App in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true

    try:
        a = App.query.filter_by(id=appId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if a is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    a.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":a.to_json()})

