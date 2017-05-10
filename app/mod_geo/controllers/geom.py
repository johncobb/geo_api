from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload

from app.mod_geo.models.geom import Geom
from app import ApiExceptionHandler as ApiException
from sqlalchemy import exc

bp_geom = Blueprint('geom', __name__, url_prefix='/geom')

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

@bp_geom.route('/<int:geomId>', methods=['GET'])
def get_geom_byid(geomId):

    """
    Query Geom.

    Parameters
    ----------
    geomId : int
        Geom Identifier

    Returns
    -------
    JSON
        Geom in JSON format
    """

    try:
        geom = Geom.query.filter_by(id=geomId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if geom is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify({"data":geom.to_json()})

@bp_geom.route('/', methods=['GET'])
def get_geoms():

    """
    Query Geoms.

    Returns
    -------
    JSON dict
        Geoms in JSON dict format
    """

    try:
        geoms = Geom.query.filter_by(archive=False).all()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(geoms) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    return jsonify({"data": [s.to_json() for s in geoms]})

@bp_geom.route('/', methods=['POST'])
def add_geom():

    """
    Add Geom.

    Parameters
    ----------
    POST : JSON
        JSON object (Geom)

    Returns
    -------
    JSON
        Geom in JSON format
    """

    data = None
    sql_geom = ''

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
            sql_geom = sql_point % (x, y)
        elif geomType == 'LineString':
            for c in coordinates:
                tmp_sql += (sql_tokens % (c[0], c[1])) + ','
            sql_geom = sql_linestring % (tmp_sql[:-1])
        elif geomType == 'Polygon':
            # Loop through dict of polygons
            for polygon in coordinates:
                # Loop through dict of coordinates
                for c in polygon:
                    # Build the sql
                    tmp_sql += (sql_tokens % (c[0], c[1])) + ', '
                    #print tmp_sql
                # Put it all together and remove the last ', '
                sql_geom += '(%s)' % (tmp_sql[:-2])
            #sql_polygon = sql_polygon % (sql_geom)
            #print sql_geom

            # Some assembly required
            sql_geom = sql_polygon % (sql_geom)
        else:
            print '*** WTF ***'

        print '***'
        print sql_geom
        print '***'
        groupId = data['properties']['groupId']
        path = data['properties']['path']

    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    # Create the object
    geom = Geom(groupId, path, geomType, sql_geom)
    #geom = Geom(groupId, path, data)

    try:
        db.session.add(geom)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    #return jsonify({"data":geom.to_json()})
    return jsonify(data)

@bp_geom.route('/<int:geomId>', methods=['PUT'])
def update_geom(geomId):

    """
    Update Geom.

    Parameters
    ----------
    geomId : int
        Geom Identifier

    Returns
    -------
    JSON
        Geom in JSON format
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
        geom = Geom.query.filter_by(id=geomId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)
    # Find the reord to update

    if geom is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT

    # Update the object
    geom.groupId = p.groupId
    geom.alias = p.alias
    geom.ip = p.ip
    geom.model = p.model
    geom.serial = p.serial
    geom.fw = p.fw

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":geom.to_json()})

@bp_geom.route('/<int:geomId>', methods=['DELETE'])
def delete_geom(geomId):

    """
    Delete Geom.

    Parameters
    ----------
    geomId : int
        Geom Identifier

    Returns
    -------
    JSON
        Geom in JSON format
    """

    # Since we never delete data just set
    # the archive flag to true
    try:
        geom = Geom.query.filter_by(id=geomId).first()
    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)


    if geom is None:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    # Update the object
    geom.archive = True

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify({"data":geom.to_json()})

