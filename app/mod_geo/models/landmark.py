from app.mod_geo.models import base
from app import db

# Define the  model
class Landmark(base.Base):
    __tablename__ = 'landmarks'

    groupId = db.Column(db.Integer, nullable=False, default=0)
    alias = db.Column(db.String(30), nullable=False)
    lat = db.Column(db.Float(10,6), nullable=False, default=0.0)
    lng = db.Column(db.Float(10,6), nullable=False, default=0.0)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, groupId, alias, lat, lng):
        self.groupId = groupId
        self.alias = alias
        self.lngsw = lat
        self.lngne = lng
        self.archive = False

    def __repr__(self):
        return '<Landmark%r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "groupId": self.groupId,
            "alias": self.alias,
            "lat": self.latne,
            "lng": self.lngne,
            "archive": self.archive
        }
