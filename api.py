
import json

import webapp2
from google.appengine.ext import ndb

from models import *

class PartnerBusinessApi(webapp2.RequestHandler):
    
    def get(self, string=None):
        key_string = string
        if key_string:
            key = ndb.Key(urlsafe=key_string)
            business = key.get()

            data = {'business': business.to_dict()}
        else:
            business_query = PartnerBusiness.query()
            businesses = [b.to_dict() for b in business_query]
            
            data = {'businesses': businesses}
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(json.dumps(data))

    def post(self):
        self.response.write(self.request.body)
