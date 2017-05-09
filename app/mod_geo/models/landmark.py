from app.mod_geo.models import base
from app import db

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from geoalchemy2 import Geometry


Base = declarative_base()


# Define the  model
#class Landmark(Base):
class Landmark(base.Base):
    __tablename__ = 'landmarks'

    groupId = db.Column(db.Integer, nullable=False, default=0)
    path = db.Column(db.String(255), nullable=False)
    #geom = db.Column(Geometry('POLYGON'))
    geom = db.Column(Geometry('POINT'))
    archive = db.Column(db.Boolean, nullable=False, default=False)
    
    def __init__(self, groupId, path, geom):
        self.groupId = groupId
        self.path = path
        self.geom = geom
        self.archive = False

    def __repr__(self):
        return '<Landmark%r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "groupId": self.groupId,
            "path": self.alias,
            "archive": self.archive
        }
