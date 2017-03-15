from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload


from app.mod_organization.models.organization import Organization

bp_organization = Blueprint('organization', __name__, url_prefix='/organization')

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_organization.route('/<int:organizationId>', methods=['GET'])
def get_organization_byid(organizationId):
    """
    Query Organization.

    Parameters
    ----------
    organizationId : int
        Organization Identifier

    Returns
    -------
    JSON
        Organization in JSON format
    """

    try:
        organization = Organization.query.filter_by(id=organizationId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    
    if organization is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":organization.to_json()})

@bp_organization.route('/', methods=['GET'])
def get_organizations():
    """
    Query Organizations.

    Returns
    -------
    JSON dict
        Organizations in JSON dict format
    """

    try:
        organizations = Organization.query.filter_by(archive=False)
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if organizations is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [o.to_json() for o in organizations]})

@bp_organization.route('/', methods=['POST'])
def add_organization():
    """
    Add Organization.

    Parameters
    ----------
    POST : JSON
        JSON object (Organization)

    Returns
    -------
    JSON
        Organization in JSON format
    """

    data = None

    # Validate the incoming JSON
    if request.json:
        data = json.dumps(request.json)
        p = Payload(data)
    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST
    
    # Create the object
    o = Organization(p.name)

    try:
        db.session.add(o)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":o.to_json()})

@bp_organization.route('/<int:organizationId>', methods=['PUT'])
def update_organization(organizationId):
    """
    Update Organization.

    Parameters
    ----------
    organizationId : int
        Organization Identifier

    Returns
    -------
    JSON
        Organization in JSON format
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
        o = Organization.query.filter_by(id=organizationId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if o is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    o.name = p.name

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":o.to_json()})

@bp_organization.route('/<int:organizationId>', methods=['DELETE'])
def delete_organization(organizationId):
    """
    Delete Organization.

    Parameters
    ----------
    organizationId : int
        Organization Identifier

    Returns
    -------
    JSON
        Organization in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true
    try:
        o = Organization.query.filter_by(id=organizationId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if o is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    # Update the object
    o.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":o.to_json()})




