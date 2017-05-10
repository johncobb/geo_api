from app.mod_geo.models import base
from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()

sql_point = 'POINT (%s %s)'
sql_linestring = 'LINESTRING (%s)'
sql_polygon = 'POLYGON (%s)'
sql_multipoint = 'MULTIPOINT (%s %s)'
sql_multilinestring = 'MULTILINESTRING (%s %s)'
sql_multipolygon = 'MULTIPOLYGON (%s %s)'
sql_geometrycollection = 'GEOMETRYCOLLECTION (%s %s)'

# Define the  model
class Geom(base.Base):
    __tablename__ = 'georeferences'

    data = []
    groupId = db.Column(db.Integer, nullable=False, default=0)
    path = db.Column(db.String(255), nullable=False)
    geom_point = db.Column(Geometry('POINT'))
    geom_linestring = db.Column(Geometry('LINESTRING'))
    geom_polygon = db.Column(Geometry('POLYGON'))
    #geomMultiPoint = db.Column(Geometry('MULTIPOINT'))
    #geomMultiLineString = db.Column(Geometry('MULTILINESTRING'))
    #geomMultiPolygon = db.Column(Geometry('MULTIPOLYGON'))
    #geomGeometryCollection = db.Column(Geometry('GEOMETRYCOLLECTION'))
    archive = db.Column(db.Boolean, nullable=False, default=False)
    
    
    def __init__(self, groupId, path, refType, sql_geo):
        self.groupId = groupId
        self.path = path

        if refType == 'Point':
            self.geom_point = sql_geo
        elif refType == 'LineString':
            self.geom_linestring = sql_geo
        elif refType == 'Polygon':
            self.geom_polygon = sql_geo
        self.archive = False

    def __repr__(self):
        return '<Geom%r>' % (self.name)

    def build_sql(self, data):

        print 'build_sql'
        geomType = data['geometry']['type']
        coordinates = data['geometry']['coordinates']

        sql_georef = ''
        tmp_sql = ''
        sql_tokens = '%s %s'

        if geomType == 'Point':
            x = coordinates[0]
            y = coordinates[1]
            sql_georef = sql_point % (x, y)
            print '***Point: ' + sql_georef
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
            print '***: WTF'


        return sql_georef

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "groupId": self.groupId,
            "path": self.alias,
            "archive": self.archive
        }

    def build_sql(self, data):
        
        geomType = data['geometry']['type']
        coordinates = data['geometry']['coordinates']

        sql_georef = ''
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

        return sql_georef
