from flask import Flask
from app import app
from app import db
import unittest
import tempfile
import json
import requests


def load_credentials(file):
    path = "unit_test/data/%s" %(file)
    json_data = None

    with open(path) as json_file:
        json_data = json.load(json_file)

    return json_data

def login_auth():
    print "login_auth"
    auth_headers  = {'Content-type': 'application/json'}

    AUTH_URL = "https://cpht.auth0.com/oauth/ro"
    AUTH_BODY = load_credentials("credentials.json")

    response = requests.post(AUTH_URL, data=json.dumps(load_credentials('credentials.json')), allow_redirects=True, headers=auth_headers)

    data = None

    if response.status_code == 200:
        data = json.loads(response.text)

    print "Auth Response"
    print "id_token: ", data['id_token']
    print "access_token: ", data['access_token']
    print "token_type: ", data['token_type']

    return "%s %s"  % (data['token_type'], data['id_token'])


class ModScannerTest(unittest.TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite+pymysql:///:memory:"
    TESTING = True

    ACCESS_TOKEN = None

    json_headers  = {'Content-type': 'application/json'}
    auth_headers  = {'Authorization': ACCESS_TOKEN}

    #@unittest.skipIf(sys.version_info < (2,6), "unsppported method in version"
    #@unittest.skip("skip test")
    def lf(self, file):
        path = "unit_test/data/%s" %(file)
        json_data = None

        with open(path) as json_file:
            json_data = json.load(json_file)

        return json_data

    def runTest(self):
        pass

    def create_app(self):
        print "create_app"
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        print "setUp"
        self.client =  app.test_client()
        self.client.testing = True
        db.create_all()

        pass


    def tearDown(self):
        print "tearDown"
        db.session.remove()
        db.drop_all()
        pass

    #@unittest.skip("skip_test")
    def test_login_auth(self):
        print "test_login_auth"
        print self.ACCESS_TOKEN

        response = self.client.get("/user/ident", headers={'Authorization': self.ACCESS_TOKEN}, follow_redirects=True)
        
        if (response.status_code == 200):
            print "Authentication Successful"
            return
        elif (response.status_code == 204):
            print "Authentication Successful"
            return
        else:
            print "Authentication Failed: %s" % (response.status_code)


    def test_mod_scanner(self):
        print "test_mod_scanner"

        # Add new record
        json_data = self.lf("scanner.json")
        response = self.client.post("/scanner/", data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)

        self.assertEquals(response.status_code, 200)
        print "Add Scanner Record"

        # Get the record
        response = self.client.get("/scanner/1")
        self.assertEquals(response.status_code, 200)
        assert b"Scanner 1" in response.data
        print "Get Scanner Record"

        # Update the record
        json_data = self.lf("_scanner.json")
        response = self.client.put("/scanner/1", data=json.dumps(json_data),
                                   follow_redirects=True,
                                   headers=self.json_headers)

        self.assertEquals(response.status_code, 200)
        # Verify the update
        response = self.client.get("/scanner/1")
        self.assertEquals(response.status_code, 200)
        assert b"(Edited)" in response.data
        print "Update Scanner Record"

        # Delete the record
        response = self.client.delete("/scanner/1")
        self.assertEquals(response.status_code, 200)
        # Verify the record delete
        response = self.client.get("/scanner/1")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        print "Delete Scanner Record"

    def test_mod_queue(self):
        print "test_mod_queue"

        # Add new record
        json_data = self.lf("doc.json")
        response = self.client.post("/queue/push",
                                    data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Add Queue Record"

        # Get the record
        response = self.client.get("/queue/1")
        self.assertEquals(response.status_code, 200)
        assert b"ScannerSerial" in response.data
        print "Get Queue Record"

        # Update the record
        json_data = self.lf("_doc.json")
        response = self.client.put("/queue/1",
                                   data=json.dumps(json_data),
                                   follow_redirects=True,
                                   headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        # Verify the update
        response = self.client.get("/queue/1")
        assert b"ScannerSerial" in response.data
        print "Update Queue Record"

        # Delete the record
        response = self.client.delete("/queue/1")
        self.assertEquals(response.status_code, 200)
        # Verify the record delete
        response = self.client.get("/queue/1")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        print "Delete Queue Record"


    def test_mod_queue_io(self):
        return
        print "test_mod_queue_io"

        # Push new record
        json_data = self.lf("doc.json")
        response = self.client.post("/queue/push",
                                    data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Push Queue Record"

        # Top record
        response = self.client.get("/queue/1/top")
        self.assertEquals(response.status_code, 200)
        print response.data
        assert b"\"status\": 1" in response.data
        print "Get Queue Record"

        # Pop record
        response = self.client.put("/queue/1/pop")
        self.assertEquals(response.status_code, 200)
        # Verify the record pop
        response = self.client.get("/queue/1/2")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        assert b"\"status\": 2" in response.data
        print "Pop Queue Record"


    def test_mod_app(self):
        print "test_mod_app"

        # Add new record
        json_data = self.lf("app.json")
        response = self.client.post("/app/", data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Add App Record"

        # Get the record
        response = self.client.get("/app/1")
        self.assertEquals(response.status_code, 200)
        assert b"Unison" in response.data
        print "Get App Record"

        # Update the record
        json_data = self.lf("_app.json")
        response = self.client.put("/app/1", data=json.dumps(json_data),
                                   follow_redirects=True,
                                   headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        # Verify the update
        response = self.client.get("/app/1")
        self.assertEquals(response.status_code, 200)
        print "Update App Record"

        # Delete the record
        response = self.client.delete("/app/1")
        self.assertEquals(response.status_code, 200)
        # Verify the record delete
        response = self.client.get("/app/1")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        print "Delete App Record"

    def test_mod_organization(self):
        print "test_mod_organization"

        # Add new record
        json_data = self.lf("organization.json")
        response = self.client.post("/organization/",
                                    data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Add Organization Record"

        # Get the record
        response = self.client.get("/organization/1")
        self.assertEquals(response.status_code, 200)
        assert b"Acme" in response.data
        print "Get Organization Record"

        # Update the record
        json_data = self.lf("_organization.json")
        response = self.client.put("/organization/1",
                                   data=json.dumps(json_data),
                                   follow_redirects=True,
                                   headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        # Verify the update
        response = self.client.get("/organization/1")
        self.assertEquals(response.status_code, 200)
        print "Update Organization Record"

        # Delete the record
        response = self.client.delete("/organization/1")
        self.assertEquals(response.status_code, 200)
        # Verify the record delete
        response = self.client.get("/organization/1")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        print "Delete Organization Record"

    def test_mod_group(self):
        print "test_mod_group"

        # Add new record
        json_data = self.lf("group.json")
        response = self.client.post("/group/",
                                    data=json.dumps(json_data),
                                    follow_redirects=True,
                                    headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        print "Add Group Record"

        # Get the record
        response = self.client.get("/group/1")
        self.assertEquals(response.status_code, 200)
        assert b"Group 1" in response.data
        print "Get Group Record"

        # Update the record
        json_data = self.lf("_group.json")
        response = self.client.put("/group/1",
                                   data=json.dumps(json_data),
                                   follow_redirects=True,
                                   headers=self.json_headers)
        self.assertEquals(response.status_code, 200)
        # Verify the update
        response = self.client.get("/group/1")
        self.assertEquals(response.status_code, 200)
        assert b"(Edited)" in response.data
        print "Update Group Record"

        # Delete the record
        response = self.client.delete("/group/1")
        self.assertEquals(response.status_code, 200)
        # Verify the record delete
        response = self.client.get("/group/1")
        self.assertEquals(response.status_code, 200)
        assert b"\"archive\": true" in response.data
        print "Delete Group Record"

if __name__ == "__main__":


    print "Running Scanner_Api UnitTests"
    print "Logging into auth provider"
    ModScannerTest.ACCESS_TOKEN = login_auth()
    print ModScannerTest.ACCESS_TOKEN
    unittest.main()

