
import unittest
import os
import json

from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2
import webtest

import dlsaa
from models import *


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
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()

        app = dlsaa.application
        self.testapp = webtest.TestApp(app)

    def tearDown(self):
        self.testbed.deactivate()

    def test_business_api_get(self):
        response = self.testapp.get('/api/business')

        # Call must succeed
        self.assertEqual(response.status_int, 200)

        data = json.loads(response.normal_body)
        self.assertTrue(data.has_key('businesses'))

    def test_business_api_post(self):
        business = PartnerBusiness()
        business.name = 'Hello World'
        business.discount_description = 'insert discount here'
        business.put()

        data_json = json.dumps(business.to_dict())
        response = self.testapp.post('/api/business', data_json)

        # Request must succeed
        self.assertEqual(response.status_int, 200)

        # Must be able to retrieve the created business
        response = self.testapp.get('/api/business/%s' % business.key.urlsafe())
        self.assertEqual(response.status_int, 200)
        returned_json = json.loads(response.normal_body)        

        self.assertTrue(returned_json.has_key('business'))
        self.assertTrue(returned_json['business']['id'], business.key.urlsafe())
