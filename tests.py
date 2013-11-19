
import unittest
import os

from google.appengine.ext import testbed
import webapp2
import webtest

import dlsaa

class BusinessApiTestCase(unittest.TestCase):

    def do_stub_setup(self):
        # from http://einaregilsson.com/unit-testing-model-classes-in-google-app-engine/
        app_id = 'dlsaa-web'
        os.environ['APPLICATION_ID'] = app_id
        datastore_file = '/dev/null'
        from google.appengine.api import apiproxy_stub_map, datastore_file_stub
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
        stub = datastore_file_stub.DatastoreFileStub(app_id, datastore_file, '/')
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

    def setUp(self):
        self.do_stub_setup()

        app = dlsaa.application
        self.testapp = webtest.TestApp(app)

    def test_business_api_get(self):
        response = self.testapp.get('/api/business')
        self.assertEqual(response.status_int, 200)
