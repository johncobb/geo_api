
from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask import _app_ctx_stack
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload
from flask_cors import CORS, cross_origin
from app import requires_auth

from app.mod_organization.models.user import User

bp_user = Blueprint('user', __name__, url_prefix='/user')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_user.route('/<int:userId>', methods=['GET'])
def get_user(userId):
    """
    Query User.

    Parameters
    ----------
    userId : int
        User Identifier

    Returns
    -------
    JSON
        User in JSON format
    """

    try:
        user = User.query.filter_by(id=userId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if user is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":user.to_json()})

@bp_user.route('/<int:userId>', methods=['GET'])
def get_users(userId):
    """
    Query Users.

    Returns
    -------
    JSON dict
        Users in JSON dict format
    """

    users = User.query.filter_by(organizationId=organizationId).filter_by(archive=False).all()

    if len(users) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [u.to_json() for u in users]})

@bp_user.route('/', methods=['POST'])
def add_user():
    """
    Add User.

    Parameters
    ----------
    POST : JSON
        JSON object (User)

    Returns
    -------
    JSON
        User in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
    # Create the object
    u = User(p.organizationId, p.first_name, p.last_name, p.email, p.phone, p.extension, p.time_zone, p.pin, p.auth_user_id)

    try:
        db.session.add(u)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":u.to_json()})

@bp_user.route('/<int:userId>', methods=['PUT'])
def update_user(userId):
    """
    Update User.

    Parameters
    ----------
    userId : int
        User Identifier

    Returns
    -------
    JSON
        User in JSON format
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
        u = User.query.filter_by(id=userId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if u is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    u.organizationId = p.organizationId
    u.first_name = p.first_name
    u.last_name = p.last_name
    u.email = p.email
    u.phone = p.phone
    u.extension = p.extension
    u.time_zone = p.time_zone
    u.pin = p.pin
    u.auth_user_id = p.auth_user_id

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":u.to_json()})

@bp_user.route('/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    """
    Delete User.

    Parameters
    ----------
    userId : int
        User Identifier

    Returns
    -------
    JSON
        User in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true

    try:
        u = User.query.filter_by(id=userId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if u is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    u.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":u.to_json()})

@bp_user.route('/auth', methods=['POST'])
def auth_user():
    """
    Authorize User.

    Parameters
    ----------
    pin : string
        User Pin

    Returns
    -------
    JSON
        User in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    try:
        user = User.query.filter_by(pin=p.pin).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if user is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":user.to_json()})


@bp_user.route('/ident', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def get_user_by_auth_user_id():
    """
    Get User By Auth UserId

    Parameters
    ----------
    pin : string
        Auth UserId

    Returns
    -------
    JSON
        User in JSON format
    """

    #pin = '007007'
    #uid = _app_ctx_stack.top.current_user['uid']

   # Get the auth_user_id
    sub = _app_ctx_stack.top.current_user['sub']
    #print "**** uid=", uid, "****"
    #print "**** sub=", sub, "****"

    try:
        #user = User.query.filter_by(id=uid).first()
        user = User.query.filter_by(auth_user_id=sub).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if user is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":user.to_json()})


@bp_user.route('/pin', methods=['PUT'])
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def update_user_pin():
    """
    Update User Pin.

    Returns
    -------
    JSON
        User in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
   
   # Get the auth_user_id
    sub = _app_ctx_stack.top.current_user['sub']

   # Find the record to update 
    try:
        u = User.query.filter_by(auth_user_id=sub).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if u is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    u.pin = p.pin

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":u.to_json()})
