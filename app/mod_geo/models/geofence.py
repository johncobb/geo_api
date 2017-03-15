from app.mod_geo.models import base
from app import db

# Define the  model
class GeoFence(base.Base):
    __tablename__ = 'geofences'

    groupId = db.Column(db.Integer, nullable=False, default=0)
    alias = db.Column(db.String(30), nullable=False)
    points = db.Column(db.String(2048), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, groupId, alias, points):
        self.groupId = groupId
        self.alias = alias
        self.points = points
        self.archive = False

    def __repr__(self):
        return '<GeoFence %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "groupId": self.groupId,
            "alias": self.alias,
            "points": self.points,
            "archive": self.archive
        }
