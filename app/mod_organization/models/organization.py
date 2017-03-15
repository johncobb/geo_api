from app.mod_organization.models import base
from app import db

class Organization(base.Base):
    __tablename__ = 'organizations'

    name = db.Column(db.String(30), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name):
        self.name = name
        self.archive = False

    def __repr__(self):
        return '<Organization %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "name": self.name,
            "archive": self.archive
        }
