
import webapp2
import json

from models import *

class PartnerBusinessApi(webapp2.RequestHandler):
    
    def get(self):
        business_query = PartnerBusiness.query()
        businesses = [b.to_dict() for b in business_query]
        
        data = {'businesses': businesses}
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(json.dumps(data))

    def post(self):
        self.response.write(self.request.body)
