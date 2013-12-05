
import unittest
import os
import json

from google.appengine.api import memcache
from google.appengine.ext import testbed
import webapp2
import webtest

import dlsaa
from models import *


class BranchApiTestCase(unittest.TestCase):

    def create_business(self):
        """
        Create a business, save it to the datastore, and return it
        """
        business = PartnerBusiness()
        business.name = 'Hello World'
        business.discount_description = 'insert discount here'
        business.put()

        return business

    def instantiate_branch_with_business(self):
        """
        Create a business, save it, then instantiate and branch and return without saving
        """
        business = self.create_business()
        branch = PartnerBranch()
        branch.address = '742 Evergreen Terrace, Springfield, USA'
        branch.location = ndb.GeoPt(14.566068, 120.992761)
        branch.business_key = business.key

        return branch

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

    def test_get(self):
        branch = self.instantiate_branch_with_business()
        branch.put()

        self.testapp.get('/api/business')

    def test_post(self):
        branch = self.instantiate_branch_with_business()
        business = branch.business_key.get()

        data_json = json.dumps(branch.to_dict())
        response = self.testapp.post('/api/branch', data_json)

        self.assertEqual(response.status_code, 200)

        self.assertIn('key', response.json)

        key_str = response.json['key']
        key = ndb.Key(urlsafe=key_str)
        createdBranch = key.get()

        # For the purposes of this test, the key doesn't matter
        branch.key = createdBranch.key
        # Check whether everything else saved correctly
        self.assertEqual(createdBranch, branch)

        related_bus = branch.business_key.get()
        self.assertEqual(business, related_bus)
