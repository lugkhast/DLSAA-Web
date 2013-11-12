
import os

import jinja2
import webapp2

import api
from models import *

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        home_template = file(os.path.join(TEMPLATE_DIR, 'home.hbs'))
        self.response.write(home_template.read())


application = webapp2.WSGIApplication([
    ('/', MainPage),

    # API stuff
    ('/api/business', api.PartnerBusinessApi),
], debug=True)
