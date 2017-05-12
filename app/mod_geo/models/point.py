from app.mod_geo.models import base
from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import JSON
Base = declarative_base()

"""
Spatial Reference System Identifier
"""
SRID = 4326 


class GeometryPoint(base.Base):

    """
    SQLALchemy table definition
    """
    #type, path, name, geometry, meta

    __tablename__ = 'geodesity_points'

    typeId = db.Column(db.Integer, nullable=False, default=0)
    path = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    #meta = db.Column(db.String(255), nullable=False)
    meta = db.Column(JSON)
    geometry = db.Column(Geometry('POINT'))
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, x, y, typeId, path, label, meta):
        self.typeId = typeId
        self.path = path
        self.label = label
        self.meta = meta
        self.geometry = 'SRID={0}; POINT ({1} {2})'.format(SRID, x, y)
        self.archive = False


