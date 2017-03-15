
# Organization dependency import(s)
from app.mod_organization.models import App
from app.mod_organization.models import Organization
from app.mod_organization.models import Group
from app.mod_scanner.models import Scanner

# App imports
from app import app
from app import db

if __name__ == "__main__":
    
    # Drop and recreate the database
    db.drop_all()
    db.create_all()
    # App
    a = App("Unison 2.0")
    db.session.add(a)
    db.session.commit()

    # Organization
    o = Organization("Acme Automotive, LLC")
    db.session.add(o)
    db.session.commit()
    
    # Group
    g = Group(o.id, "Group 1")
    db.session.add(g)
    db.session.commit()
    
    # Scanner
    s = Scanner(g.id, "Scanner 1", "192.168.1.100", "Zebra TC75", "1F2A3218", "1.0")
    db.session.add(s)
    db.session.commit()

    print a.to_json()
    print o.to_json()
    print g.to_json()
    print s.to_json()
    db.session.commit()






