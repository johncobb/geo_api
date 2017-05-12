from flask import Flask
from flask import json
from flask import jsonify
from flask import Blueprint, flash, g, session
from flask import request, redirect, url_for, render_template
from flask_api import status
from app import db
from app import JSON_API_Message as API_MSG
from app import Payload as Payload


from geoalchemy2 import Geometry
from geoalchemy2.functions import GenericFunction

from app.mod_geo.models.point import GeometryPoint
from app import ApiExceptionHandler as ApiException
from sqlalchemy import exc
from sqlalchemy import func


bp_geometry = Blueprint('geometry', __name__, url_prefix='/geometry')

sql_point = 'POINT ({0} {1})'

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_geometry.route('/', methods=['POST'])
def add_point():

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
        
        typeId = data['properties']['typeId']
        path = data['properties']['path']
        label = data['properties']['label']
        meta = data['properties']['meta']
        geometry_type = data['geometry']['type']
        coordinates = data['geometry']['coordinates']

        tmp_sql = ''
        sql_tokens = '%s %s'

        if geometry_type == 'Point':
            x = coordinates[0]
            y = coordinates[1]
            
        else:
            raise ApiException('Expecting type: Point', status_code=status.HTTP_400_BAD_REQUEST)

    else:
        return jsonify(API_MSG.JSON_400_BAD_REQUEST), status.HTTP_400_BAD_REQUEST

    # Create the object
    #point = GeometryPoint(x, y, groupId, name, path)
    point = GeometryPoint(x, y, typeId, path, label, meta)

    try:
        db.session.add(point)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify(data)


@bp_geometry.route('/nearbybrief', methods=['GET'])
def nearbybrief():

    """
    Query Nearby.

    Parameters
    -----------
    geomId : int
        Geom Identifier

    Returns
    -------
    JSON
        Geom in JSON format
    """

    try:
        features = []
        """ Query All Columns """
        points = db.session.query(GeometryPoint).all()

        """ Query Geometry Column Only """
        #points = db.session.query(GeometryPoint.geometry).all()

        """ Query Geometry Column and return GeoJSON """
        points = db.session.query(GeometryPoint.geometry.ST_AsGeoJSON()).all()
        
        """ Query Selected Columns and return GeoJSON """
        #points = db.session.query(GeometryPoint.path, GeometryPoint.groupId, GeometryPoint.geometry.ST_AsGeoJSON()).all()
        for p in points:

            point_feature = {
                'type': 'Feature',
                'geometry': json.loads(p[0])
            }

            features.append(point_feature)

        geojson_points = {
            'type': 'FeatureCollection',
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:4326'
                }
            },
            'features': features
        }


    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(points) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify(geojson_points)


@bp_geometry.route('/nearby', methods=['GET'])
def nearby():

    """
    Query Nearby.

    Parameters
    -----------
    geomId : int
        Geom Identifier

    Returns
    -------
    JSON
        Geom in JSON format
    """

    try:
        features = []
        """ Query All Columns """
        #points = db.session.query(GeometryPoint).all()

        """ Query Geometry Column Only """
        #points = db.session.query(GeometryPoint.geometry).all()

        """ Query Geometry Column and return GeoJSON """
        #points = db.session.query(GeometryPoint.geometry.ST_AsGeoJSON()).all()
        
        """ Query Selected Columns and return GeoJSON """
        points = db.session.query(GeometryPoint.geometry.ST_AsGeoJSON(), GeometryPoint.meta, GeometryPoint.label, GeometryPoint.path, GeometryPoint.typeId, GeometryPoint.id, GeometryPoint.archive).all()

        for p in points:

            properties = {
                'id' : p.id,
                'typeId': p.typeId,
                'path': p.path,
                'label': p.label,
                'meta': p.meta,
                'archive': p.archive
            }

            point_feature = {
                'type': 'Feature',
                'properties': properties,
                'geometry': json.loads(p[0]) # Must access as string index 0
            }

            features.append(point_feature)

        geojson_points = {
            'type': 'FeatureCollection',
            'crs': {
                'type': 'name',
                'properties': {
                    'name': 'EPSG:4326'
                }
            },
            'features': features
        }


    except exc.SQLAlchemyError as e:
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    if len(points) == 0:
        return jsonify(API_MSG.JSON_204_NO_CONTENT), status.HTTP_204_NO_CONTENT
    
    return jsonify(geojson_points)


