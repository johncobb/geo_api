from app.mod_geo.models import base
from app import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

Base = declarative_base()

"""
Spatial Reference System Identifier
"""
SRID = 4326 


class GeometryPoint(base.Base):

    """
    SQLALchemy table definition
    """

    __tablename__ = 'geodesity_points'

    groupId = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    geometry = db.Column(Geometry('POINT'))
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, x, y, groupId, name,  path):
        self.grouId = groupId
        self.name = name
        self.path = path
        self.geometry = 'SRID={0}; POINT ({1} {2})'.format(SRID, x, y)
        self.archive = False


