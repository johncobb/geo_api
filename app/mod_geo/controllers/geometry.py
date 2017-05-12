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

SRID = 4326 


"""
GeoSpatialNotes:

ST_Distance({0} {1})
SRID={0}; POINT ({1} {2})
"""

# GET retrieve a record
# PUT update a record
# POST a new record
# PATCH partially update record
# DELETE delete a record

@bp_geometry.route('/', methods=['POST'])
def add():

    """
    Add GeometryPoint.

    Parameters
    ----------
    POST : JSON
        GeoJSON object (GeometryPoint)

    Returns
    -------
    JSON
        GeoPoint in GeoJSON format
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


@bp_geometry.route('/', methods=['PUT'])
def update():

    """
    Update GeometryPoint.

    Parameters
    ----------
    PUT : JSON
        GeoJSON object (GeometryPoint)

    Returns
    -------
    JSON
        GeoPoint in GeoJSON format
    """

    data = None
    sql_geom = ''

    # Validate the incoming JSON
    if request.json:
        data = request.get_json()
        
        pointId = data['properties']['id']
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

    try:

        gp = GeometryPoint.query.filter_by(id=pointId).first()

        gp.typeId = typeId
        gp.path = path
        gp.label = label
        gp.meta = meta
        gp.geometry = "SRID={0}; POINT ({1} {2})".format(SRID, x, y)
        
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        raise ApiException(e.message, status_code=status.HTTP_400_BAD_REQUEST)

    return jsonify(data)
@bp_geometry.route('/nearby', methods=['GET'])
def nearby():

    """
    Query Nearby.

    Returns
    -------
    JSON
        Points in GeoJSON format
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


@bp_geometry.route('/dist', methods=['GET'])
def dist():

    """
    Query Distance.

    Returns
    -------
    JSON
        Points in GeoJSON format
    """

    try:

        features = []
        
        sql_point = 'SRID={0}; POINT ({1} {2})'

        x = 37.000
        y = -87.00
        sql_point = sql_point.format(SRID, x, y)
        
        points = db.session.query(GeometryPoint.geometry.ST_AsGeoJSON(), func.ST_Distance(sql_point, GeometryPoint.geometry), GeometryPoint.meta, GeometryPoint.label, GeometryPoint.path, GeometryPoint.typeId, GeometryPoint.id, GeometryPoint.archive).all()


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
                'geometry': json.loads(p[0]), # Must access as string index 0
                'dist': p[1] # Must access as string index 0
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
