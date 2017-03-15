"""
Available arguments:
    -r n: Add n records for printer 1 to the database
    -i  : Run the initalization method. If called multiple times duplicate
          records may be added.
    -h  : Prints this docstring
"""
import requests
import json
from flask import Flask
import unittest
import tempfile
import sys
import getopt

from unittest import TestCase


#json_headers  = {'Content-type': 'application/json'}
json_headers  = {'Content-type': 'application/json', 'Authorization': 'bearer '}
url = "http://localhost:8181%s"

def lf(file):
    path = "unit_test/data/%s" %(file)
    json_data = None

    with open(path) as json_file:
        json_data = json.load(json_file)

    return json_data

def post_json(json_data, route):
    return requests.post(route,
                         data=json.dumps(json_data),
                         allow_redirects=True,
                         headers=json_headers)

def init_db():
    print "Add App Record"
    print post_json(lf("app.json"), url % "/app/").status_code

    print "Add Applet Record"
    print post_json(lf("applet.json"), url % "/applet/").status_code

    print "Add Organization Record"
    print post_json(lf("organization.json"), url % "/organization/").status_code

    print "Add User Record"
    print post_json(lf("user.json"), url % "/user/").status_code

    print "Add Group Record"
    print post_json(lf("group.json"), url % "/group/").status_code

    print "Add Scanner Record"
    print post_json(lf("scanner.json"), url % "/scanner/").status_code

    print "Add Scanner Applet Record"
    print post_json(lf("scanner_applet.json"), url % "/scanner/applet").status_code

    print "Add Queue Record"
    print post_json(lf("doc.json"), url % "/queue/push").status_code

if __name__ == "__main__":
    try:
        options = getopt.getopt(sys.argv[1:], "hr:i", [])
        argmap = {arg:val for arg, val in options[0]}
        if '-i' in argmap:
            init_db()

        if '-r' in argmap:
            for i in xrange(int(argmap['-r'])):
                post_json(lf("doc.json"), url % "/queue/push")
            print "Added " + argmap['-r'] + " queued records to the database."

        if '-h' in argmap:
            print(__doc__)

    except (getopt.GetoptError, ValueError):
        print "Invalid argument detected"
        print(__doc__)
