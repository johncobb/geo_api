from app.mod_organization.models import base
from app import db

class User(base.Base):
    __tablename__ = 'users'
    
    organizationId = db.Column(db.Integer, nullable=False, default=0)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    extension = db.Column(db.String(8), nullable=False)
    time_zone = db.Column(db.Integer, nullable=False, default=0)
    pin = db.Column(db.String(6), nullable=False)
    auth_user_id = db.Column(db.String(50), nullable=False)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, organizationId, first_name, last_name, email, phone, extension, time_zone, pin, auth_user_id):
        self.organizationId = organizationId
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.extension = extension
        self.time_zone = time_zone
        self.pin = pin
        self.auth_user_id = auth_user_id
        self.archive = False

    def __repr__(self):
        return '<User %r>' % (self.name)

    def to_json(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "organizationId": self.organizationId,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "extension`": self.extension,
            "time_zone": self.time_zone,
            "pin": self.pin,
            "auth_user_id": self.auth_user_id,
            "archive": self.archive
        }
