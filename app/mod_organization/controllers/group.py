from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload


from app.mod_organization.models.group import Group

bp_group = Blueprint('group', __name__, url_prefix='/group')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_group.route('/<int:groupId>', methods=['GET'])
def get_group(groupId):
    """
    Query Group.

    Parameters
    ----------
    groupId : int
        Group Identifier

    Returns
    -------
    JSON
        Group in JSON format
    """

    try:
        group = Group.query.filter_by(id=groupId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if group is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    content = {"data":group.to_json()}
    return jsonify(content)

@bp_group.route('/', methods=['POST'])
def add_group():
    """
    Add Group.

    Parameters
    ----------
    POST : JSON
        JSON object (Group)

    Returns
    -------
    JSON
        Group in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
    # Create the object
    g = Group(p.organizationId, p.name)

    try:
        db.session.add(g)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":g.to_json()})

@bp_group.route('/<int:groupId>', methods=['PUT'])
def update_group(groupId):
    """
    Update Group.

    Parameters
    ----------
    groupId : int
        Group Identifier

    Returns
    -------
    JSON
        Group in JSON format
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
        g = Group.query.filter_by(id=groupId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    
    if g is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    g.name = p.name

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    
    return jsonify({"data":g.to_json()})

@bp_group.route('/<int:groupId>', methods=['DELETE'])
def delete_group(groupId):
    """
    Delete Group.

    Parameters
    ----------
    groupId : int
        Group Identifier

    Returns
    -------
    JSON
        Group in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true

    try:
        g = Group.query.filter_by(id=groupId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if g is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    g.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":g.to_json()})


@bp_group.route('/<int:groupId>/scanners', methods=['GET'])
def get_scanners_by_groupid(groupId):
    """
    Query Scanners by Group.

    Scanners
    ----------
    groupId : int
        Scanner Identifier

    Returns
    -------
    JSON dict
        Scanners in JSON dict format
    """

    try:
        scanners = Scanner.query.filter_by(groupId=groupId).filter_by(archive=False).all()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(scanners) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [s.to_json() for s in scanners]})


