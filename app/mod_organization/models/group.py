from app.mod_organization.models import base
from app import db

class Group(base.Base):
    __tablename__ = 'groups'

    organizationId = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, organizationId, name):
        self.organizationId = organizationId
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<Group %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "organizationId": self.organizationId,
            "name": self.name,
            "archive": self.archive
        }
