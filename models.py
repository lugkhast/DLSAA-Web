
from google.appengine.ext import ndb

# DLSAA Card partner locator stuff
# ---------------------------------------------------------
class PartnerBusiness(ndb.Model):
    name = ndb.StringProperty()
    discount_description = ndb.StringProperty()


class PartnerBranch(ndb.Model):
    location = ndb.GeoPtProperty()


# Chapter locator
# ---------------------------------------------------------


class Chapter(ndb.Model):
    name = ndb.StringProperty()
    has_address = ndb.BooleanProperty()
    address = ndb.StringProperty()


class Officer(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.EmailProperty()
    mobile_number = ndb.PhoneNumberProperty()


# News and events
# ---------------------------------------------------------
class NewsArticle(ndb.Model):
    title = ndb.StringProperty()
    body = ndb.StringProperty()
