from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload

from app.mod_geo.models.georef import GeoRef
from app import ApiExceptionHandler as ApiException
from sqlalchemy import exc

bp_georef = Blueprint('georef', __name__, url_prefix='/georef')

sql_point = 'POINT (%s %s)'
sql_linestring = 'LINESTRING (%s)'
sql_polygon = 'POLYGON (%s)'
sql_multipoint = 'MULTIPOINT (%s %s)'
sql_multilinestring = 'MULTILINESTRING (%s %s)'
sql_multipolygon = 'MULTIPOLYGON (%s %s)'
sql_geometrycollection = 'GEOMETRYCOLLECTION (%s %s)'

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_georef.route('/<int:georefId>', methods=['GET'])
def get_georef_byid(georefId):

    """
    Query GeoRef.

    Parameters
    ----------
    georefId : int
        GeoRef Identifier

    Returns
    -------
    JSON
        GeoRef in JSON format
    """

    try:
        georef = GeoRef.query.filter_by(id=georefId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if georef is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":georef.to_json()})

@bp_georef.route('/', methods=['GET'])
def get_georefs():

    """
    Query GeoRefs.

    Returns
    -------
    JSON dict
        GeoRefs in JSON dict format
    """

    try:
        georefs = GeoRef.query.filter_by(archive=False).all()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(georefs) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [s.to_json() for s in georefs]})

@bp_georef.route('/', methods=['POST'])
def add_georef():

    """
    Add GeoRef.

    Parameters
    ----------
    POST : JSON
        JSON object (GeoRef)

    Returns
    -------
    JSON
        GeoRef in JSON format
    """

    data = None
    sql_georef = ''

    # Validate the incoming JSON
    if request.json:
        data = request.get_json()
        
        geomType = data['geometry']['type']
        coordinates = data['geometry']['coordinates']
        tmp_sql = ''
        sql_tokens = '%s %s'

        if geomType == 'Point':
            x = coordinates[0]
            y = coordinates[1]
            sql_georef = sql_point % (x, y)
        elif geomType == 'LineString':
            for c in coordinates:
                tmp_sql += (sql_tokens % (c[0], c[1])) + ','
            sql_georef = sql_linestring % (tmp_sql[:-1])
        elif geomType == 'Polygon':
            # Loop through dict of polygons
            for polygon in coordinates:
                # Loop through dict of coordinates
                for c in polygon:
                    # Build the sql
                    tmp_sql += (sql_tokens % (c[0], c[1])) + ', '
                    #print tmp_sql
                # Put it all together and remove the last ', '
                sql_georef += '(%s)' % (tmp_sql[:-2])
            #sql_polygon = sql_polygon % (sql_georef)
            #print sql_georef

            # Some assembly required
            sql_georef = sql_polygon % (sql_georef)
        else:
            print '*** WTF ***'

        print '***'
        print sql_georef
        print '***'
        groupId = data['properties']['groupId']
        path = data['properties']['path']

    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    # Create the object
    georef = GeoRef(groupId, path, geomType, sql_georef)
    #georef = GeoRef(groupId, path, data)

    try:
        db.session.add(georef)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    #return jsonify({"data":georef.to_json()})
    return jsonify(data)

@bp_georef.route('/<int:georefId>', methods=['PUT'])
def update_georef(georefId):

    """
    Update GeoRef.

    Parameters
    ----------
    georefId : int
        GeoRef Identifier

    Returns
    -------
    JSON
        GeoRef in JSON format
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
        georef = GeoRef.query.filter_by(id=georefId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    # Find the reord to update

    if georef is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    georef.groupId = p.groupId
    georef.alias = p.alias
    georef.ip = p.ip
    georef.model = p.model
    georef.serial = p.serial
    georef.fw = p.fw

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":georef.to_json()})

@bp_georef.route('/<int:georefId>', methods=['DELETE'])
def delete_georef(georefId):

    """
    Delete GeoRef.

    Parameters
    ----------
    georefId : int
        GeoRef Identifier

    Returns
    -------
    JSON
        GeoRef in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true
    try:
        georef = GeoRef.query.filter_by(id=georefId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)


    if georef is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    # Update the object
    georef.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":georef.to_json()})

