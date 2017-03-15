from app.mod_organization.models import base
from app import db

# Define the  model
class Applet(base.Base):
    __tablename__ = 'applets'

    appId = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, appId, name):
        self.appId = appId
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<App %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "appId": self.appId,
            "name": self.name,
            "archive": self.archive
        }
